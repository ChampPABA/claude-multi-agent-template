# CI/CD pipeline reference

The concrete shape of both pipelines, the secrets each repo needs, retention,
rollback, and the backup system. Values use a fictional org `acme`
(`acme/web`, `acme/api`, bucket `acme-backup`) — substitute the real org.

Contents: Assumptions and free-plan budget · Frontend pipeline · Backend
pipeline (deploy.yml jobs, Host recovery, Host disk, Concurrency and
timeouts) · Secrets inventory · Retention and scanning · Rollback pinning ·
Backups · VPS layout · VPS access.

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

**Worked examples** (real repos, read `.github/workflows/deploy.yml`,
`prune-ghcr.yml` and `docker-compose.yml` at these commits):
`aaa-portal/api` @ `3519daf` and `aspect-education/api` @ `fba4852`. The
deploy-by-sha shape below is proven on aspect prod (run 34695329134, all
named steps green incl. the public `/version` check) and aaa dev (deploy run
34728653721: four named steps green, probes 200→200 / 404→404; prune apply
run 34728805886: first proven DELETE with `GITHUB_TOKEN`). As of 2026-09-13
the aaa retag had not yet run on prod. Neither matches every rule here: aaa
checks image hygiene after push, has no public `/version` step and files the
failure issue on `failure()` only; aspect scans only `:main` and pulls every
service. Where they differ, this file states the standard.

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
3. **Build locally, check, then push** — two `docker/build-push-action`
   steps around the hygiene check, so an image that fails it never gets a
   GHCR tag (push-then-check leaves a tagged bad image in the registry when
   the check fails):
   - **Build** with `load: true` and only the `sha-<commit>` tag.
     `cache-from: type=gha` + `cache-to: type=gha,mode=max` (Actions cache is
     a separate free 10GB pool; `type=registry` would store layers in GHCR
     and eat the 500MB. `mode=max` is load-bearing: deps stages are not in
     the final image chain, so `mode=min` caches nothing useful). Cache is
     per-branch and evicts after 7 days untouched — the first build after a
     lockfile change or a quiet week is cold. Expected, not a regression.
   - **Image hygiene**: run the local image and assert no devDeps tools are
     in `node_modules` (`drizzle-kit`, `eslint`, `typescript`, …) — fails the
     build instead of shipping a bloated runner if someone "simplifies" the
     install flags. A failed `docker run` must fail the step, not read as
     "clean" (`set -euo pipefail`, capture the listing before grepping).
   - **Push** with `push: true`, `cache-from: type=gha`, both tags and
     `provenance: false` (without it buildx publishes an OCI index plus an
     attestation manifest, and one build lands as three package versions —
     nothing consumes them and they distort retention). Same inputs on the
     same builder, so every layer is a cache hit.
   - Both builds pass `build-args: GIT_SHA=${{ github.sha }}` (served by
     `/version`) and `labels: org.opencontainers.image.source=https://github.com/<org>/api`.
     The label links the GHCR package to the repo on first push, so the
     package inherits the repo's access and the repo's workflows get
     automatic access to it (see Retention for why the prune needs that).
     Identical inputs on both builds keep the push a cache hit.
4. Tags: `ghcr.io/<org>/api:sha-<commit>` and `ghcr.io/<org>/api:<branch>`.
   **The deploy runs `sha-<commit>`**, never the branch tag: a branch tag can
   move between the push that started the job and the pull. The branch tag
   exists for the prune (it keeps whatever the branch tags resolve through)
   and the trivy scan; on the host it is re-pointed locally after each
   verified deploy (see Host recovery).

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
3. Four **named** `appleboy/ssh-action` steps, not one script, so a failed
   run names the stage that failed ("Wait for health", not "Deploy"). Nothing
   carries over between ssh sessions, so every step that runs `docker
   compose` exports `IMAGE_TAG=sha-${{ github.sha }}` itself. A step that
   forgets does not fail: under the retag standard `.env` names the branch,
   so it silently acts on the host's `:<branch>`, the PREVIOUS verified build
   until the retag runs (only the blank-`.env` alternative fails loud).

   **"Pull, migrate and switch"** — the only step that receives
   `GHCR_PULL_TOKEN` (`env:` + `envs:`), in order:
   - `export IMAGE_TAG=sha-${{ github.sha }}` — overrides whatever `.env`
     names; the deploy always runs the immutable build.
   - `chmod +x` + `sha256sum` the shipped backup script (scp preserves modes
     unreliably; the hash pins the shipped bytes in the log).
   - **Ephemeral registry login**: `DOCKER_CONFIG=$(mktemp -d)`, `trap 'rm -rf`
     on EXIT, `docker login` with `GHCR_PULL_TOKEN` (a PAT with
     `read:packages`) piped via `--password-stdin`. Never `docker logout` at
     script end and never a persistent login — the shared `~/.docker` store
     once got wiped mid-deploy by a sibling deploy, leaving recovery with no
     credential.
   - **Deploy-time probes, baseline**: before touching anything, curl 1–2 real
     endpoints (e.g. `/health` and one real query path) and `tee` the status
     codes into `.probe-baseline` in the deploy root — not a guessable `/tmp`
     path on a shared host. Rank responses `2xx=0 < 404=1 < 5xx/unreachable=2`.
   - `docker compose pull --policy always api`. The api service sets
     `pull_policy: missing` (so a manual recreate needs no credential), and
     `pull` honours that field: without the flag a tag already on the host is
     never re-fetched (e.g. a re-run build re-pushing the same sha tag). Name
     the service: an unscoped pull also re-fetches floating tags like
     `postgres:17-alpine`, and if the upstream digest moved, `up -d` then
     recreates the database mid-deploy.
   - `timeout 120 docker compose run -T --rm api <migrate-cmd>` — migrate with
     the NEW image before any new code serves traffic; the one-off container
     leaves the running stack untouched, so a failed migration ends the deploy
     before the switch. The ceiling exists because DDL stuck on a lock would
     otherwise hang the job with no output and no failure.
   - `docker compose up -d`.

   **"Wait for health"** — poll the service itself, `curl /health` in a
   bounded loop (~60s); on timeout print `docker compose ps` + `logs
   --tail=20` and fail. Not `docker compose ps` as the check (orchestrator
   "healthy" is a weaker claim than the service answering, and parsing its
   JSON output has bitten before).

   **"Verify /version sha"** — `/version` must return `${{ github.sha }}`.
   This is the difference between "CI green" and "deployed".

   **"Re-probe against baseline"** — a missing or empty `.probe-baseline`
   fails the step (a lost hand-off must not read as "nothing regressed").
   Re-probe the same paths; any probe that got WORSE fails the deploy — the
   sha check sees the image, not the serving behaviour. Improvement (was down,
   now answers) passes. `rm -f .probe-baseline`, then, only after the
   comparison passed:
   - `docker tag ghcr.io/<org>/api:sha-<commit> ghcr.io/<org>/api:<branch>` —
     re-point the host's local branch tag at the build just verified (see Host
     recovery). A failed deploy never reaches this line, so the tag stays on
     the last good build.
   - `docker image prune -f || true` — tolerated because it runs after
     verification (a busy daemon's non-zero must not report a verified deploy
     as failed). It does **not** bound host disk: sha-tagged images never go
     dangling, so every deploy leaves one more image behind. Open gap, see
     Host disk.
4. **"Verify public /version"** (runner-side, whenever the api sits behind a
   tunnel or reverse proxy): curl the public URL from the runner in a short
   retry loop (~6 × 5s, `Cache-Control: no-cache`) and compare to the commit.
   The host-side check proves the container; this proves the route to it.
5. **Deploy-failure issue** (`if: failure() || cancelled()`): open-or-comment
   an issue titled `deploy failure: <env>` with label `deploy-failure` — `gh
   label create ... || true`, exact-title search over open issues, comment
   throttled to at most hourly (re-runs carry the same evidence; the issue
   stays open until a deploy succeeds). `cancelled()` is load-bearing: a job
   that hits `timeout-minutes` concludes `cancelled`, not `failure`, so
   `failure()` alone stays silent on exactly the hung deploy. Deploy
   concurrency never cancels a running deploy, so `cancelled` here means a
   timeout or a manual cancel. Scoped to the deploy jobs only: a gate/build
   failure means someone is at the keyboard; the issue exists for a deploy
   that breaks after CI was green.

### Host recovery: manual recreate without a deploy

Standard: **retag after verification** (the aaa-portal/api shape). The stack
`.env` keeps `IMAGE_TAG=<branch>` (`development` / `main`); the compose file
keeps `image: ghcr.io/<org>/api:${IMAGE_TAG:?...}` and `pull_policy:
missing`; the re-probe step re-points the host's `:<branch>` at the verified
sha. Result: a hand `docker compose up -d` (no deploy running, no registry
credential) recreates on the last verified build, and bare `docker compose
ps` / `logs` work without exporting anything.

Why the retag exists: once deploys pull by sha, nothing else moves the host's
local branch tag. Without it, `.env` names whatever build that tag held
before the switch, and a manual recreate silently starts a stale image.

Two consequences the runbook must state:

- The host's `:<branch>` and GHCR's `:<branch>` differ. GHCR's is the newest
  BUILD (possibly one whose deploy failed); the host's is the last verified
  deploy. Never pull the branch tag by hand (`docker compose pull --policy
  always`, or `docker pull ghcr.io/<org>/api:<branch>`): either overwrites
  the local tag with GHCR's newest build, possibly an unverified one. (A bare
  `docker compose pull` honours `pull_policy: missing` and skips the tag
  already present.) To pull by hand, export `IMAGE_TAG=sha-<commit>` first.
- Keep `${IMAGE_TAG:?}` in the compose file: a `.env` missing the key fails
  loud instead of defaulting to some tag.

Alternative, not the standard (the aspect-education/api shape): `.env` holds
`IMAGE_TAG` empty, so every compose command fails until the operator exports
the sha (read from `docker inspect` of the running container). It cannot
start a stale build, but every manual command needs the sha, and a recreate
needs someone who knows where to find it. An audit accepts either shape; a
`.env` naming the branch with NO retag in the deploy is a fail.

### Host disk (open gap)

Sha-tagged images never become dangling, so `docker image prune -f` frees
none of them and host disk grows by one api image per deploy. Tracked as
aaa-portal/api#90; aspect-education/api has the same gap and keeps the images
on purpose as local rollback candidates. Do not claim the post-deploy prune
bounds disk.

Candidate fix, **unproven** (verify on dev before adopting):
`docker image prune -af --filter "label=org.opencontainers.image.source=https://github.com/<org>/api" --filter "until=<window>"`.
`-a` removes tagged images no container uses; the label filter is what keeps
it from also deleting every other unused image on the shared host (it needs
the build label above); `until` keeps rollback candidates built inside the
window. Docker has no built-in "keep the last N". A pinned environment runs
its pinned image, so it is in use and survives.

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
| api | `GHCR_PULL_TOKEN` | PAT `read:packages` only (the prune uses `GITHUB_TOKEN`) | the deploy's "Pull, migrate and switch" step only |
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
- The prune and its trivy scan run on the job's own `GITHUB_TOKEN`
  (`permissions: contents: read, packages: write`); trivy's registry login is
  `-u ${{ github.actor }}`. No PAT. Deleting a package version needs
  **admin** on the package, not just `packages: write`: the repo has it
  because its own workflow published the package (the publisher gets admin),
  and the `org.opencontainers.image.source` label links package to repo so
  the access is inherited. A package first pushed some other way (by hand, by
  another repo) needs the repo granted Admin in the package settings, or the
  DELETE fails. Proven: aaa-portal/api prune apply run 34728805886 deleted a
  version with `GITHUB_TOKEN` (aspect has only proven LIST).
- trivy CRITICAL scan (`--exit-code 1 --ignore-unfixed`) of both `:main` and
  `:development` (both run on the host) rides the prune run —
  detection latency up to a week, deliberately NOT a build gate. When the base
  image changes shape (new runtime major), run report-only first and arm from
  a clean baseline; a permanently red weekly cron is an observability black
  hole.
- First prune after changing KEEP: dry-run manually (workflow_dispatch without
  apply) to see the plan before it deletes.

## Rollback pinning

A CI deploy always runs its own `sha-<commit>`, whatever `.env` says, so a
pin governs manual recreates, not the next push. Pinning is three steps:

1. Set `IMAGE_TAG=sha-<commit>` in that environment's `.env` on the VPS and
   `docker compose up -d`.
2. Add a `pinned-<env>` tag to that version in GHCR. The prune protects
   `main`, `development` and every `pinned-*` tag — a bare `sha-` pin ages out
   of the retention window while the environment still runs it, and a later
   manual recreate on a host that no longer holds that image fails its pull
   with `manifest unknown`.
3. Stop deploys to that branch while pinned (hold pushes, or disable the
   deploy job). The next push deploys its own sha over the pin, and the
   stale pin in `.env` then rolls the environment back on the next manual
   recreate.

Unpinning is two steps: delete the `pinned-<env>` tag **and** set `IMAGE_TAG`
back to the branch name. A pin left in `.env` resurfaces on the next manual
recreate, silently rolling back past every deploy since.

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

## VPS access

- **Tag the node** (`tag:<project>-vps`). Tagged nodes don't key-expire; a
  user-owned node's key does, and on expiry the host drops off the tailnet:
  every SSH-touching workflow fails with `dial tcp <host>:22: i/o timeout`
  while the public site (via the tunnel) stays up, so nothing else alerts.
- **ACL**: allow `tag:ci` → `tag:<project>-vps:22`. Once the node is tagged,
  `autogroup:self` no longer covers it, so the rule must name the tag. Add an
  `ssh` rule only if Tailscale SSH is used; it is optional, and
  `appleboy/ssh-action` still authenticates with `VPS_SSH_KEY`.
- **Firewall**: UFW default deny incoming; 22/tcp allowed only on
  `tailscale0`; web via Cloudflare Tunnel, so no public ports.
- **Break-glass**: the provider's VNC console, not public-IP SSH. At setup,
  log in at the console with the password once, then store the credentials in
  the password manager. A path never logged into does not count.
