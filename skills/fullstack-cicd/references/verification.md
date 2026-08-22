# Verification and audit reference

How to check the standard is actually met — probe toolkit, the compliance
checklist, and the report format. Everything here is read-only.

Two boundaries, restated:

- **Read-only only.** list / get / head / status checks. Any mutation (create,
  set, delete, rotate) is a finding to propose, not an action to take.
- **Never read or print secret values.** Probe by name and by behaviour. A
  token that 200s its own bucket and 403s others is correctly scoped — no
  value needs to be seen by anyone.

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

`bucket list` compared against the inventory doc is the orphan check: any
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

Expected: **200 on its own bucket, 403 on any other bucket**. Anything else is
a scope finding. This exact signing shape (`aws:amz:auto:s3`) is what works
against R2 with a dashboard-created token.

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

Frontend equivalent — confirm the Pages deployment landed via the wrangler CLI
(a green CI job proves the upload ran, not that Pages serves it):

```
wrangler pages deployment list --project-name=<org>-web[-dev]
```

Newest row must match the pushed branch and deploy time.

### Backup probes (on the VPS, or via the backup-health workflow)

```
ls -t ~/backups/<prod-db>_*.sql.gz | head -1     # newest dump
stat -c %Y <that file>                            # age <= 25h?
grep -E '^Backup (completed|FAILED):' ~/backups/backup.log | tail -1
```

Fresh file AND last status `completed` — the status line is what proves the
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
- [ ] Gate job (typecheck/lint/unit vs real Postgres) gates both branches, in step with test.yml
- [ ] Secret scan (gitleaks) gates the build
- [ ] Every job sets `timeout-minutes`
- [ ] Deploy concurrency queues (`cancel-in-progress: false`); PR workflows cancel
- [ ] Docs-only pushes skip CI (paths-ignore)
- [ ] Image hygiene: no devDeps in the runtime image
- [ ] Registry login is ephemeral (temp DOCKER_CONFIG, trap-cleanup), never persists on host

**Pipeline (web repo)**

- [ ] Gate job on development/main pushes, explicit-result `needs` check so feature previews survive
- [ ] wrangler-action deploys to prod project (main) / dev project (else); previews on branch
- [ ] Deploy verified via wrangler CLI: newest `pages deployment list` row matches the push
- [ ] `CLOUDFLARE_API_TOKEN` + `CLOUDFLARE_ACCOUNT_ID` secrets present

**Retention / rollback**

- [ ] Weekly prune cron active; keeps N + active branch tags + `pinned-*`, manifest-graph-aware
- [ ] trivy scan rides the prune run (not a build gate)
- [ ] Any pinned environment has BOTH the `.env` `IMAGE_TAG` and a `pinned-<env>` GHCR tag

**R2 / tokens**

- [ ] Exactly one `<org>-backup` bucket; environments are prefixes, not buckets
- [ ] Lifecycle rules: prod 365d / dev 30d / blobs 90d / multipart-abort present
- [ ] Exactly one live S3 token (`<org>-backup-rw`), scope probe passes (200 own / 403 others)
- [ ] One Pages token (`<org>-pages`); no `-migration` token left over
- [ ] CORS rule present if browser uploads exist
- [ ] `R2_KEY_PREFIX` set wherever R2 is configured; app fails at boot without it
- [ ] No bucket or token exists that the inventory doesn't list (and vice versa)

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
