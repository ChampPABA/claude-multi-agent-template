# CI/CD pipeline reference

The concrete shape of both pipelines, the secrets each repo needs, retention,
rollback, and the backup system. Values use a fictional org `acme`
(`acme/web`, `acme/api`, bucket `acme-backup`) — substitute the real org.

## Assumptions and free-plan budget

- GitHub org on the **Free** plan: 2,000 Actions minutes/month, 500MB GHCR
  storage, **no branch protection** (Team+ feature). The spending limit at $0
  means exceeding GHCR storage **blocks image pushes** mid-deploy — it does not
  bill. That, not cost, is the failure mode retention guards.
- One VPS, two compose stacks on it (dev + prod). CI reaches it over Tailscale.
- Consequences the standard accepts: PR discipline replaces branch protection;
  a gate job duplicated inside deploy.yml replaces required checks; GHCR
  retention is an active prune job, not a passive setting.

## Frontend pipeline (web repo)

Two workflows: `test.yml` (PR-only) and `deploy.yml`.

**deploy.yml shape:**

- Trigger: push to any branch, with `paths-ignore: ['**.md', '.gitignore',
  'LICENSE']` — docs-only pushes deploy nothing.
- `concurrency: group: cf-pages-${{ github.ref_name }}`,
  `cancel-in-progress: false` — deploys queue, never vanish.
- **gate** job: `if: github.ref_name == 'development' || github.ref_name == 'main'`
  — typecheck + lint + test on direct pushes to the deploy branches. Skipped on
  feature branches (test.yml already covers the PR event; gating there would
  run the suite twice per push). Mirrors the api gate; keep the two in step.
- **build-deploy** job: `needs: [gate]` with an explicit result check:

  ```yaml
  if: '!cancelled() && (needs.gate.result == ''success'' || needs.gate.result == ''skipped'')'
  ```

  The explicit check is required: a skipped `needs` job skips its dependents
  too, so a plain `needs: [gate]` would kill every feature-branch preview.
  Runs when the gate passed or was skipped; a failed/cancelled gate deploys
  nothing. The leading `!` must stay quoted — bare, YAML parses it as a tag.

- Deploy step is `cloudflare/wrangler-action` with:

  ```
  apiToken:   ${{ secrets.CLOUDFLARE_API_TOKEN }}     # the <org>-pages token
  accountId:  ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
  command:    pages deploy <build-output> \
               --project-name=${{ github.ref_name == 'main' && '<org>-web' || '<org>-web-dev' }} \
               --branch=${{ github.ref_name }}
  ```

  Two Pages projects: prod (`main`) and dev (everything else); any non-dev
  branch under the dev project is a preview at `<branch>.pages.dev`.
- Build-time env differs per branch (e.g. `VITE_API_URL`: empty on main where
  prod hostname is baked in, `secrets.DEV_API_URL` otherwise).
- **Verify the deploy landed** — a green build job proves the upload ran, not
  that Pages serves it. Final step in build-deploy (or the audit probe):

  ```
  wrangler pages deployment list --project-name=<org>-web[-dev]
  ```

  The newest row must match the pushed branch (and the deploy time this run);
  anything else is a failed deploy. Same token as the deploy step.

**web repo secrets:** `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`,
`DEV_API_URL`.

## Backend pipeline (api repo)

Workflows: `test.yml` (PR gate), `deploy.yml` (build + deploy), `prune-ghcr.yml`
(retention + CVE scan), plus scheduled health checks (see Backups).

### deploy.yml jobs

**Gate job** (typecheck/lint/unit). No `if:` — runs for both branches. Free orgs
cannot require checks and main is reachable without a PR (direct push, UI edit,
revert button), so this job is what actually gates production. It runs the suite
against a real Postgres service container (`postgres:17-alpine`, health-cmd
`pg_isready`, mapped port, `DATABASE_URL` env) because most test files hit a
real database — a suite without one gates nothing. The job is a deliberate
duplicate of test.yml's unit job; editing one without the other silently
changes what gates a deploy.

**build-and-push job:**

1. Secret scan gates the build: gitleaks via docker, `--no-git --redact`,
   exit non-zero on hits. Pre-commit hooks are a nice-to-have, not a boundary.
2. GHCR login with the automatic `GITHUB_TOKEN` (`packages:write`) — no
   extra secret needed to push.
3. `docker/build-push-action` with `provenance: false` (without it buildx
   publishes an OCI index plus an attestation manifest, and one build lands as
   three package versions — nothing consumes them and they distort retention),
   `cache-from: type=gha` + `cache-to: type=gha,mode=max` (Actions cache is a
   separate free 10GB pool; `type=registry` would store layers in GHCR and eat
   the 500MB. `mode=max` is load-bearing: deps stages are not in the final
   image chain, so `mode=min` caches nothing useful). Cache is per-branch and
   evicts after 7 days untouched — the first build after a lockfile change or a
   quiet week is cold. Expected, not a regression.
4. Tags: `ghcr.io/<org>/api:sha-<commit>` and `ghcr.io/<org>/api:<branch>`.
5. Optional image-hygiene step: pull the fresh image and assert no devDeps
   tools are present (`drizzle-kit`, `eslint`, `typescript`, …) — fails the
   build instead of shipping a bloated runner if someone "simplifies" the
   install flags.

**Prerequisites the api itself must provide** — the deploy verification below
stands on two endpoints; a project missing them is incomplete, not "done
except cosmetics":

- `GET /health` — liveness with no dependencies beyond the process answering.
- `GET /version` — returns the build's commit sha. The image takes the sha as
  a build arg (e.g. `GIT_SHA`) and serves it; the deploy script compares this
  against `${{ github.sha }}`. Without it there is no way to tell which build
  is actually live.

**deploy-dev / deploy-prod jobs** (`if:` on branch name, `needs: [gate,
build-and-push]`, GitHub `environment:` set for each):

1. Connect to Tailscale (`tailscale/github-action@v4`, OAuth client id/secret,
   `tags: tag:ci`) — the SSH targets are Tailscale names.
2. `appleboy/scp-action` ships `docker-compose.yml` and the backup script from
   the repo to the deploy root (`/srv/<org>-dev` / `/srv/<org>-prod`),
   `overwrite: true` (without it an existing file is left in place and the
   step is a no-op). The repo copy is canonical: the deploy is what carries
   config changes to the host; a host-side edit is overwritten at its own
   risk. `.env` is the exception — hand-managed per environment.
3. `appleboy/ssh-action` deploy script, in order:
   - `chmod +x` + `sha256sum` the shipped backup script (scp preserves modes
     unreliably; the hash pins the shipped bytes in the log).
   - **Ephemeral registry login**: `DOCKER_CONFIG=$(mktemp -d)`, `trap 'rm -rf`
     on EXIT, `docker login` with `GHCR_PULL_TOKEN` (a PAT with
     `read:packages`) piped via `--password-stdin`. Never `docker logout` at
     script end and never a persistent login — the shared `~/.docker` store
     once got wiped mid-deploy by a sibling deploy, leaving recovery with no
     credential.
   - **Deploy-time probes, baseline**: before touching anything, curl 1–2 real
     endpoints (e.g. `/health` and one real query path) and save the status
     codes. Rank responses `2xx=0 < 404=1 < 5xx/unreachable=2`. After the
     switch, re-probe: any probe that got WORSE fails the deploy — the sha
     check below sees the image, not the serving behaviour. Improvement
     (was down, now answers) passes.
   - `docker compose pull --policy always api` — a moved branch tag is never
     fetched without the flag.
   - `timeout 120 docker compose run -T --rm api <migrate-cmd>` — migrate with
     the NEW image before any new code serves traffic; the one-off container
     leaves the running stack untouched, so a failed migration ends the deploy
     before the switch. The ceiling exists because DDL stuck on a lock would
     otherwise hang the job with no output and no failure.
   - `docker compose up -d`.
   - Poll the service itself — `curl /health` in a bounded loop (~60s) — not
     `docker compose ps` (orchestrator "healthy" is a weaker claim than the
     service answering, and parsing its JSON output has bitten before).
   - Verify `/version` returns the build's commit sha. This is the difference
     between "CI green" and "deployed".
   - Re-probe and compare against the baseline (above).
   - `docker image prune -f || true` — tolerated because it runs after
     verification.
4. **Deploy-failure issue** (`if: failure()`): open-or-comment an issue titled
   `deploy failure: <env>` with label `deploy-failure` — `gh label create
   ... || true`, exact-title search over open issues, comment throttled to at
   most hourly (re-runs carry the same evidence; the issue stays open until a
   deploy succeeds). Scoped to the deploy jobs only: a gate/build failure
   means someone is at the keyboard; the issue exists for a deploy that breaks
   after CI was green.

### Concurrency and timeouts

- deploy.yml: `cancel-in-progress: false` (deploys queue).
- PR workflows: `cancel-in-progress: true` (superseded runs vanish).
- Every job: `timeout-minutes` tiered ~10 (web build) / 15 (gate, build,
  deploy) / 20 (long jobs) against real run times.

## Secrets inventory

| Repo | Secret | Holds | Used by |
|---|---|---|---|
| api | `TS_OAUTH_CLIENT_ID` / `TS_OAUTH_SECRET` | Tailscale OAuth client | every SSH-touching workflow |
| api | `VPS_HOST` / `VPS_USER` / `VPS_SSH_KEY` | deploy target | deploy + health workflows |
| api | `GHCR_PULL_TOKEN` | PAT `read:packages` (+ `delete:packages` if the prune runs in CI) | VPS image pulls |
| api | `R2_ACCESS_KEY_ID` / `R2_SECRET_ACCESS_KEY` | the `<org>-backup-rw` S3 token | backup-health / checks that read R2 |
| web | `CLOUDFLARE_API_TOKEN` | the `<org>-pages` token | wrangler-action |
| web | `CLOUDFLARE_ACCOUNT_ID` | account id | wrangler-action |
| web | `DEV_API_URL` | dev api origin | dev/preview builds |

On the VPS the same R2 token values live in the deploy-root `.env`s (both
stacks) and in `~/.backups/.r2-backup.env` for the backup cron. Values are
never written into any doc or repo — only names and where each lives.

## Retention and scanning

- Weekly prune cron keeps the N newest images per package plus every active
  branch tag and every `pinned-*` tag, failing closed over the manifest
  reference graph (an image referenced by a kept manifest is kept, even if
  older than N).
- `KEEP ≈ floor(500MB × 0.8 ÷ unique-layer-growth per build)`. Only raise it
  after checking the org billing page, and only on evidence.
- trivy CRITICAL scan (`--exit-code 1 --ignore-unfixed`) rides the prune run —
  detection latency up to a week, deliberately NOT a build gate. When the base
  image changes shape (new runtime major), run report-only first and arm from
  a clean baseline; a permanently red weekly cron is an observability black
  hole.
- First prune after changing KEEP: dry-run manually (workflow_dispatch without
  apply) to see the plan before it deletes.

## Rollback pinning

Two steps, not one: set `IMAGE_TAG=sha-<commit>` in that environment's `.env`
on the VPS **and** add a `pinned-<env>` tag to that version in GHCR. The prune
protects `main`, `development` and every `pinned-*` tag — a bare `sha-` pin
ages out of the retention window while the environment is still running it,
and the next deploy fails its pull with `manifest unknown`, mid-deploy.

## Backups and retention of the data, not the images

Nightly script (canonical copy in the api repo; the deploy ships it to the
host, the host crontab runs the deployed copy — one tested artifact, no drift):

- Per database: `docker exec <db-container> pg_dump -U <user> <db> | gzip >
  ~/backups/<db>_<UTC-ts>.sql.gz`.
- **Fail loud**: exit non-zero and print `Backup FAILED` on any dump error, any
  undersized dump (size floor ~1KB — catches an empty-but-successful pg_dump),
  or any offsite failure. Cron only appends to a log; without this a broken
  backup stays invisible (once for a month).
- **Offsite to R2**: PUT via `curl --aws-sigv4 "aws:amz:auto:s3"` with the S3
  token, then HEAD the object and compare `content-length` to the local size —
  a 200 PUT is not proof the object landed intact. Upload happens before local
  rotation so a failed upload never coincides with pruning local history.
- **Local rotation per database** (`find -name '<db>_*.sql.gz' -mtime +N
  -delete`), days tuned per database — sizes can differ by orders of magnitude
  between databases on the same host, so one global window fits none.
- R2-side retention is NOT the script's job: bucket lifecycle rules own it
  (see `r2-tokens.md`). The upload is PUT-only, no delete credential needed.
- Credentials live in `~/.backups/.r2-backup.env` (sourced with `set -a`),
  not in the script. Missing file = warn and skip offsite; the local backup is
  still valid on its own.

**Backup-health** (scheduled GH Actions, morning after the backup window):
SSH to the VPS and check two things — newest dump file age ≤ 25h (catches dead
cron, broken script, silent no-file failure) and the last status line in
backup.log is `completed`, not `FAILED` (a fresh file alone does not prove the
offsite leg worked). Non-zero exit = red workflow = the incident channel.

A schedule that fires a few hours after the backup window surfaces a failure
the same morning, with margin under the 25h net if the schedule slips.

## VPS layout

```
/srv/<org>-dev/     dev stack: docker-compose.yml, backup script, .env (hand-managed)
/srv/<org>-prod/    prod stack: same shape
~/backups/          dumps, backup.log, .r2-backup.env (offsite credentials)
```

No separate staging environment: `development` on the same VPS is staging.
