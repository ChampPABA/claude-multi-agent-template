# R2 buckets and tokens reference

Naming grammar, lifecycle, token creation, CORS, the new-project setup order,
and the migration runbook. Examples use a fictional org `acme`.

## Naming grammar

One grammar, one greppable prefix per org — searching `<org>-` finds the whole
family:

```
<org>-backup            the org's single bucket (structure = prefixes inside)
<org>-backup-rw         the single R2 S3 token (Object Read & Write, that bucket only)
<org>-backup-migration  temp token for consolidations; deleted when done
<org>-pages             the single account API token (Pages: Edit)
```

Env/secret names that carry the credentials:

```
R2_ACCESS_KEY_ID / R2_SECRET_ACCESS_KEY   the S3 token (CI + deploy-root .env)
R2_KEY_PREFIX                             env separator inside the shared bucket
CLOUDFLARE_API_TOKEN                      wrangler-convention secret holding the Pages token
```

## Bucket layout and lifecycle defaults

Structure inside `<org>-backup` — environments are prefixes, never buckets:

```
postgres/<env>/YYYY/MM/DD/<env>-<UTC ts>.sql.gz   DB dumps
documents/<env>/...                               user files, no expiry
screenshots/<userId>/<ts>.jpg                     live blobs (not backups), 90d
```

Default lifecycle (date-partitioned keys keep per-env rules expressible):

| Prefix | Expire | Why |
|---|---|---|
| `postgres/prod/` | 365d | a year of restore points for production |
| `postgres/dev/` | 30d | dev history is cheap insurance, not archive |
| `screenshots/` (blobs) | 90d | live content with bounded lifetime |
| `documents/` | no expiry | user data — deletion is a product decision, never a lifecycle one |
| (default) multipart-abort | 7d | incomplete uploads must not accrue forever |

Rules the hard way taught:

- **One bucket, structure by prefix.** Bucket-per-env once orphaned a token
  scope when buckets were recreated under new names; uploads were dead for six
  weeks before anyone noticed. One bucket = one thing to scope a token to, and
  the token survives environment restructuring.
- **The lifecycle ruleset PUT replaces everything and rejects rules without a
  transition.** Use `wrangler r2 bucket lifecycle add <bucket> <name> <prefix>`
  (merges), verify with `lifecycle list`, and always keep the multipart-abort
  rule that ships by default.
- **Two credentials per org, no more.** Read/write separation is traded away
  deliberately: audit and revoke happen at one point per type. If write-only
  hardening is ever needed again, split a read-only checker token off; nothing
  else changes.

## Creating tokens (dashboard-only, both kinds)

R2 S3 tokens and Pages tokens **cannot be created via the API**:

- `POST /accounts/{id}/tokens` returns a bearer `value` that does not sign S3
  requests — every sigv4 call fails with SignatureDoesNotMatch. S3 tokens from
  the dashboard work; API-issued ones do not.
- The IAM permission-group list has no Pages group, so a Pages-scoped token
  cannot be expressed through the API at all.

So budget exactly two dashboard clicks per org; everything else is CLI-able:

1. **S3 token**: dashboard → R2 → Manage R2 API Tokens → Create API Token.
   Name `<org>-backup-rw`, permission Object Read & Write, scope: this bucket
   only (`<org>-backup`). Yields an access-key-id + secret pair.
2. **Pages token**: dashboard → My Profile → API Tokens → Create Custom Token.
   Name `<org>-pages`, permission Account → Cloudflare Pages → Edit, account
   scope: this account only.

Store the S3 pair as `R2_ACCESS_KEY_ID`/`R2_SECRET_ACCESS_KEY` in the VPS
deploy-root `.env`s and as same-named GitHub secrets; store the Pages token as
GitHub secret `CLOUDFLARE_API_TOKEN` on the web repo. Never write values into
docs or chats — the inventory records names, scopes and where each lives.

## CORS for browser uploads

Browser uploads are presigned PUTs straight to R2, so the bucket needs a CORS
rule BEFORE any browser traffic switches to it. A missing rule fails as a
network `TypeError` (CORS-blocked), not a 403 — server-side tests pass and only
a real browser UAT catches it.

Set via a JSON file (R2-native lowercase keys, each rule nested in an
`allowed` object, the whole thing wrapped in `{"rules": [...]}`):

```json
{
  "rules": [
    {
      "allowed": {
        "origins": ["https://app.example.com", "https://dev.example.com"],
        "methods": ["PUT", "GET", "HEAD"],
        "headers": ["content-type"]
      },
      "maxAgeSeconds": 3600
    }
  ]
}
```

```
wrangler r2 bucket cors set <org>-backup --file cors.json
wrangler r2 bucket cors list <org>-backup
```

## The `R2_KEY_PREFIX` contract

Whenever R2 is configured in the app, `R2_KEY_PREFIX` must be set — and the
app should throw at boot if it is missing. Without it, one environment's files
silently land in the other's namespace; with it, dev and prod share one bucket
safely because every key is namespaced (`documents/dev/...` vs
`documents/prod/...`). Fail loud at boot beats corrupting a namespace for
weeks.

## New-project setup (ordered)

1. **Bucket**: `wrangler r2 bucket create <org>-backup` (same location hint as
   the org's other buckets).
2. **Lifecycle**: add the rules from the table above one by one via
   `lifecycle add`; verify with `lifecycle list` that every prefix rule is
   present AND the multipart-abort default survived.
3. **CORS** (only if browser uploads exist): set + list per above, before any
   cutover.
4. **S3 token** (dashboard): per Creating tokens. Distribute to `.env`s and
   GitHub secrets.
5. **Pages token** (dashboard): per Creating tokens. GitHub secret
   `CLOUDFLARE_API_TOKEN` on the web repo.
6. **Verify the token scope** with the sigv4 probe from `verification.md`:
   200 on its own bucket, 403 on any other. Do this before anything depends
   on it.
7. **Inventory row**: record bucket + both tokens (names, scopes, where the
   values live) in the project's inventory doc. No inventory row, no token —
   this rule is what catches dead orphans on later cleanup passes.

## Migration runbook (merge/consolidate buckets)

The order below is load-bearing. Out of order it produces wrongly-prefixed
objects no lifecycle rule covers, a crash-loop window, or unrecoverable data
loss. Read the whole runbook before starting.

1. **Prepare the target**: new bucket + full lifecycle rules (+ CORS if
   browser uploads) per New-project setup above.
2. **Temp migration token** (dashboard): `<org>-backup-migration`, Object
   Read & Write, scoped to BOTH old and new buckets. It gets deleted at the
   end — that is what keeps the two-token end state true.
3. **Copy**: `rclone copy` old bucket roots into the new bucket root. First
   INSPECT the old key layout (`rclone lsd` / the REST listing from
   verification.md) and pick the mapping:
   - keys already carry env prefixes (`postgres/prod/...`) → root-to-root
     copy, keys land where lifecycle rules expect them;
   - keys are flat or bucket-per-env (`prod.sql.gz` in a per-env bucket) →
     map each old bucket into its prefix (`rclone copy old: nova-backup:
     postgres/prod/` style), or the objects arrive outside every lifecycle
     rule and never expire.
   Either way the end state must be: every object under its `postgres/<env>/`
   (or blob) prefix in the new bucket.
4. **Verify**: `rclone size` old vs new must match before anything switches.
5. **Deploy the script before flipping the backup env.** The new backup
   script (writing correctly-prefixed keys) must be live on the host BEFORE
   `.r2-backup.env` points at the new bucket — the old script against the new
   bucket writes wrongly-prefixed objects no lifecycle rule covers.
6. **Pre-flip the app `.env` before promote.** Add the new R2 vars to the app
   `.env` and deploy the running image first: the old image ignores the extra
   vars, the new image requires them. Flipping at promote time instead opens a
   crash-loop window where the new image boots without its config.
7. **Switch the backup env** (`.r2-backup.env` → new bucket) and the app env;
   restart dev first, verify, then prod.
8. **Re-run the copy once more** to catch stragglers written during the
   switch window.
9. **Wait for a scheduled backup cycle to land in the new bucket**, verified
   (fresh object, size-verified by the backup script; see cicd-pipeline.md).
10. **Only now delete**: empty and delete the old buckets, delete the
    `-migration` token and every replaced token, shred local staging files
    from the copy.
11. **Update the inventory**: removed artifacts struck out, new ones recorded.
    Then verify the end state: exactly one bucket, one S3 token, one Pages
    token for the org.

## Inventory table template

Keep this in the project's handbook/inventory doc; values never appear, only
names, scopes, and where each credential lives:

| artifact | type | scope | used by | lives in |
|---|---|---|---|---|
| `<org>-backup` | bucket | prefix lifecycles per table above | everything below | R2 |
| `<org>-backup-rw` | R2 S3 token | Object R&W, this bucket only | backup cron, app, CI | VPS `.env`s + GH secrets |
| `<org>-pages` | account API token | Pages: Edit | web deploys | GH secret on web repo |
