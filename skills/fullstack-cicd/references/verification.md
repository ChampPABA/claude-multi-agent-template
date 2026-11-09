# Verification and audit reference

How to check the standard is actually met — probe toolkit, the compliance
checklist, and the report format. Everything here is read-only.

Two boundaries, restated:

- **Read-only only.** list / get / head / status checks. Any mutation (create,
  set, delete, rotate, the CI reachability probe) is a finding to propose, not
  an action to take.
- **Never read or print secret values.** Probe by name and by behaviour. A
  token that 200s its own bucket and 403s others is correctly scoped — no
  value needs to be seen by anyone. Two copies of a value compare by sha256
  prefix (`sha256sum | cut -c1-8`); never cat, grep or sed a secrets file to
  the terminal.

## Probe toolkit

### GitHub (needs `gh` auth)

```
gh secret list --repo <org>/<repo>        # which secret NAMES exist (never values)
gh workflow list --repo <org>/<repo>      # expected workflows present + active
gh run list --repo <org>/<repo> --limit 5 # recent runs green?
```

What each proves: secrets exist by name; the expected workflows (test, deploy,
prune, backup-health) exist and are not disabled; deploys actually run.

### R2 via wrangler (needs `wrangler login`)

```
wrangler r2 bucket list                     # full bucket inventory — orphan detection
wrangler r2 bucket info <bucket>            # object_count, total size
wrangler r2 bucket lifecycle list <bucket>  # every prefix rule + multipart-abort present?
wrangler r2 bucket cors list <bucket>       # browser-upload rule present?
wrangler pages project list                 # Pages projects: prod + dev exist?
```

`bucket list` compared against the inventory is the orphan check: any
bucket not in the inventory is a finding; any inventory row with no bucket is
a finding. `bucket info` gives the numbers for "is the new bucket actually
receiving backups" (object_count rising daily).

### Token scope probe (sigv4, the cheap authoritative one)

With the S3 token's key/secret available in the environment:

```
curl -s -o /dev/null -w '%{http_code}' \
  --aws-sigv4 "aws:amz:auto:s3" \
  --user "$R2_ACCESS_KEY_ID:$R2_SECRET_ACCESS_KEY" \
  "https://<account_id>.r2.cloudflarestorage.com/<bucket>/<known-key>"
```

A new, empty bucket has no known key (404): use the bucket root with
`?list-type=2` instead. Expected: **200 on its own bucket, 403 on any other bucket**. Anything else is
a scope finding. This exact signing shape (`aws:amz:auto:s3`) is what works
against R2.

### Object listing WITHOUT an S3 token (mystery-object hunting)

The account REST API lists a bucket's objects with a plain OAuth bearer —
no S3 token needed. This is how unexplained objects inside a bucket get
enumerated and proven deletable:

```
curl -s -H "Authorization: Bearer <wrangler-oauth-token>" \
  "https://api.cloudflare.com/client/v4/accounts/<account_id>/r2/buckets/<bucket>/objects"
```

The bearer is wrangler's own OAuth token (from `wrangler login`; `wrangler
whoami` shows it, and it lives in wrangler's local config). Paginate if the
response indicates more.

### Live service probes

```
curl -s https://<api-host>/health     # service answers at all
curl -s https://<api-host>/version    # deployed sha == expected commit?
```

The pair is the definition of "deployed": answering, and answering with the
build you think is live. On the VPS the same probes run against
`localhost:$API_PORT` (read the port from the deploy-root `.env`). If either
endpoint does not exist, that is itself a finding — the standard's deploy
verification stands on both, so "api has no /health or /version" goes in the
report as a fail with "add the endpoints" as the fix.

Host image state (on the VPS, read-only):

```
docker inspect --format '{{.Image}}' <api-container>          # image the api runs
docker image inspect --format '{{.Id}}' ghcr.io/<org>/api:<branch>
docker images ghcr.io/<org>/api ; df -h /var/lib/docker       # image count, free space
```

The first two IDs must match: the local branch tag names the running,
verified build, so a manual recreate starts it. A mismatch on a stack whose
`.env` names the branch means the retag is missing, or the last deploy failed
after its switch (the running build never passed verification).

Frontend equivalent — confirm the Pages deployment landed via the wrangler CLI
(a green CI job proves the upload ran, not that Pages serves it):

```
wrangler pages deployment list --project-name=<org>-web[-dev]
```

Newest row must match the pushed branch and deploy time.

### VPS access probes

```
tailscale status --json         # the VPS node: tagged, no KeyExpiry
sudo ufw status verbose          # on the VPS: default deny (incoming), 22/tcp on tailscale0 only
```

Or the Tailscale admin console: machine → "Key expiry: disabled".

**CI reachability probe** — proves the path CI actually uses, which reading
the ACL does not. A push-triggered workflow on a temp branch: tailnet join as
`tag:ci` → `tailscale ping <vps>` → tcp 22 → ssh with `VPS_SSH_KEY` →
`docker login` with a temp `DOCKER_CONFIG` → `docker manifest inspect` on a
private image. About a minute of Actions; delete the branch after. It pushes
and runs a workflow, so in an audit it waits for approval; in setup it is the
VPS-access verify step.

Host state (on the VPS, read-only):

```
docker compose ls -a                               # project names + config paths, stopped ones too: any collision?
docker volume ls                                   # every stack's volumes named, none orphaned
ls -a /srv/*/ /srv/*/*/ | grep -E '\.bak'          # stale secret copies (.env.bak-*, *.bak-*)
grep -rlE '(KEY|SECRET|TOKEN)[^=]*=[^$]' <host configs>   # file names only, never -o or the match
```

### Backup probes (on the VPS, or via the backup-health workflow)

```
ls -t ~/backups/<org>/<prod-db>_*.sql.gz | head -1     # newest dump
stat -c %Y <that file>                            # age <= 25h?
grep -E '^Backup (completed|FAILED):' ~/backups/<org>/backup.log | tail -1
```

An existing host's own path counts (rule 16). Fresh file AND last status `completed` — the status line is what proves the
offsite leg worked; a fresh file alone does not.

## Compliance checklist

Walk every row; each needs a verdict. "Unknown" (no credentials to verify) is
a valid verdict — report it rather than guessing. The checklist is a floor,
not a ceiling: a real audit also reports anything ELSE discovered along the
way (a hardcoded value that contradicts the inventory, a name no config file
could produce) — anything you'd flag if the checklist didn't exist. And every
finding must cite the evidence it rests on — the file, line, or probe output
that shows it. A finding you can't point at is a hunch; leave it out or mark
it explicitly as unverified.

**Pipeline (api repo)**

- [ ] Deploy = pull pre-built image; no build step on the VPS
- [ ] Migrate runs between pull and `up -d`, as a one-off, with a timeout
- [ ] Deploy verifies `/health` then `/version` sha before reporting success
- [ ] The api exposes `/health` and `/version` (sha) at all — missing endpoints are a fail, not a nicety
- [ ] Gate job gates both branches by calling test.yml (`workflow_call`, typecheck/lint/unit vs real Postgres); no second copy of the gate
- [ ] Gate skips checks a merged PR already ran (cicd-pipeline.md): after the first merge the gate log shows "PR #N head <sha>: tree matches, Test success" plus the skipped steps, the deployed `/version` (web: Pages deployment source) equals the pushed sha, and the live web bundle holds the real api URL
- [ ] Secret scan (gitleaks) gates the build
- [ ] Every job sets `timeout-minutes`
- [ ] Deploy concurrency queues (`cancel-in-progress: false`); PR workflows cancel
- [ ] Docs-only pushes skip CI (paths-ignore)
- [ ] Image hygiene: no devDeps in the runtime image
- [ ] Registry login is ephemeral (temp DOCKER_CONFIG, trap-cleanup), never persists on host
- [ ] Deploy runs `sha-<commit>`: every compose-running ssh step exports `IMAGE_TAG=sha-${{ github.sha }}`; nothing deploys the branch tag
- [ ] Deploy is split into named ssh steps (pull/migrate/switch → wait for health → verify /version → re-probe), baseline handed off via `.probe-baseline` in the deploy root, and a missing baseline fails
- [ ] `GHCR_PULL_TOKEN` reaches only the pull step (no `envs: GHCR_TOKEN` on the other steps)
- [ ] `compose pull --policy always api` names the api service
- [ ] Image hygiene runs on a local `load: true` build before the push; the image carries the `org.opencontainers.image.source` label
- [ ] Deploy-failure issue fires on `failure() || cancelled()` (a timeout concludes `cancelled`)
- [ ] Public `/version` verified from the runner when the api sits behind a tunnel/proxy
- [ ] Host recovery: the deploy retags the host's `:<branch>` to the verified sha after re-probe (standard), or `.env` holds `IMAGE_TAG` empty (accepted alternative). `.env` naming the branch with no retag is a fail: a manual recreate starts a stale build

A repo still on the old shape shows up as: no `IMAGE_TAG` export in the deploy
script (it pulls the branch tag), one ssh-action doing everything, the prune
reading a PAT secret, and `GHCR_PULL_TOKEN` documented with `delete:packages`.

**VPS access**

- [ ] VPS tailnet node tagged `tag:<project>-vps`: admin shows key expiry "disabled", or `tailscale status --json` shows no KeyExpiry for it
- [ ] ACL lets `tag:ci` reach `tag:<project>-vps` on 22 (plus an `ssh` rule only if Tailscale SSH is used)
- [ ] UFW: default deny incoming, 22/tcp allowed only on `tailscale0`, no public ports (web via Cloudflare Tunnel)
- [ ] Break-glass console (provider VNC) logged into with its password at least once; credentials in the password manager
- [ ] CI reachability probe passed (or proposed, in an audit)

**Host (shared by several orgs)**

- [ ] Compose project names unique on the host (`docker compose ls -a`), set via top-level `name:`; volumes named explicitly and `external: true`
- [ ] Container names unique per host
- [ ] Names follow what exists (rule 16): a name off the standard pattern that collides with nothing is pass; a collision is fail
- [ ] Host configs read secrets from env; no literal secret in any config file (a hardcoded key is missed on rotation)
- [ ] No stale secret copies on the host (`.env.bak-*`, `*.bak-*`)
- [ ] Session cookies host-only, a distinct cookie prefix per app and env; no parent-domain cookie when the parent domain hosts more than one app

**Pipeline (web repo)**

- [ ] Gate job on development/main pushes calls test.yml (no copy), explicit-result `needs` check so feature previews survive
- [ ] test.yml cancels superseded runs only on `pull_request`, so a called gate queues instead of blocking the deploy
- [ ] If tests are sharded: the count lives once (matrix list + `strategy.job-total`), shard test counts sum to an unsharded run, and a failing shard has been shown to stop build-deploy
- [ ] wrangler-action deploys to prod project (main) / dev project (else); previews on branch
- [ ] Deploy verified via wrangler CLI: newest `pages deployment list` row matches the push
- [ ] `CLOUDFLARE_API_TOKEN` + `CLOUDFLARE_ACCOUNT_ID` secrets present
- [ ] Pages hostnames come from the API's `subdomain`, not an assumed `<project>.pages.dev`

**Retention / rollback**

- [ ] Weekly prune cron active; keeps N + active branch tags + `pinned-*`, manifest-graph-aware
- [ ] Prune and trivy run on `GITHUB_TOKEN` (`packages: write`), no PAT; `GHCR_PULL_TOKEN` scoped `read:packages` only
- [ ] trivy scan of `:main` and `:development` rides the prune run (not a build gate)
- [ ] Any pinned environment has the `.env` `IMAGE_TAG`, a `pinned-<env>` GHCR tag, AND its deploys held; no unpinned environment has a leftover `sha-` in `.env` or a stale `pinned-*` tag
- [ ] Host disk: api image count and free space reported (sha images never dangle, so `image prune -f` does not bound them); warn until a label-scoped prune is proven (aaa-portal/api#90)

**R2 / tokens**

- [ ] Exactly one `<org>-backup` bucket; environments are prefixes, not buckets
- [ ] Lifecycle rules: prod 365d / dev 30d / blobs 90d / multipart-abort present
- [ ] Exactly one live S3 token (`<org>-backup-rw`), scope probe passes (200 own / 403 others)
- [ ] One Pages token (`<org>-pages`); no `-migration` token left over
- [ ] Both are Account API Tokens, not user tokens; every temp token has an expiry
- [ ] One of each CI credential per org (Tailscale OAuth client, SSH deploy key, GHCR PAT), each repo holding a copy; no per-repo duplicates
- [ ] CORS rule present if browser uploads exist
- [ ] `R2_KEY_PREFIX` set wherever R2 is configured; app fails at boot without it
- [ ] Inventory exists (Hindsight `Inventory: <org> CI/CD credentials`, or the project's own inventory file) and lists every bucket, token, key and secret with the repos holding a copy; nothing live is missing from it, and no row is missing from live
- [ ] Bucket names still referenced in configs or scripts exist in `bucket list`; a reference to a gone or other-org bucket is a finding

**Backups**

- [ ] Nightly cron live; script is the repo-canonical copy (hash matches the deployed one)
- [ ] Fail-loud: dump error / undersized file / offsite failure all exit non-zero
- [ ] Offsite upload size-verified (HEAD content-length), uploaded before local rotation
- [ ] Local rotation per database, days tuned per DB
- [ ] backup-health cron green: newest dump ≤ 25h AND last status `completed`
- [ ] At least one restore drill has happened (a backup never restored is a hope)

## Report format

ALWAYS use this exact template:

```
# Compliance audit — <project> (<date>)

## Summary
<N of M> checks pass. Biggest gaps: <one line naming the worst 1–3 findings>.

## Findings
| # | Area | Check | Expected | Found | Verdict | Fix |
|---|------|-------|----------|-------|---------|-----|

Verdicts: pass · fail · warn (works but drifts from standard) · unknown (no access to verify).

## Recommended next actions
Ordered by risk. Each one names the exact command/change, and any mutation
waits for explicit approval.
```

Rules for the report itself:

- One row per checklist item that is not a clean pass — clean passes collapse
  into the summary count. The table is for what needs eyes.
- Every `fail`/`warn` row's Fix must be concrete enough to run as-is (command
  or edit), because that is what happens next.
- Findings that require a mutation are proposed here and nowhere executed.
