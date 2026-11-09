---
name: fullstack-cicd
description: >-
  End-to-end standard for standing up, extending, or auditing a full-stack project's
  infrastructure: GitHub Actions CI/CD on the Free org plan, Cloudflare Pages frontend
  deploys, GHCR + VPS immutable-image backend deploys, one R2 bucket per org with
  lifecycle rules, exactly two Cloudflare account tokens, and nightly database
  backups with health-check crons. Use whenever the task is setting up a new project's
  pipeline from scratch ("set up CI/CD", "ตั้ง project ใหม่", "deploy หน้าบ้านหลังบ้านให้ครบ"),
  adding R2 storage or backups, creating or rotating Cloudflare tokens, migrating or
  consolidating R2 buckets, or auditing an existing project against this standard
  ("ตรวจว่า pipeline ครบไหม", "what am I missing to deploy properly"). Also use for any
  question touching R2 buckets, R2 S3 tokens, Pages API tokens, wrangler r2
  lifecycle/cors, GHCR retention, deploy-pipeline shape, or a slow CI test gate
  ("test ช้า", "CI ช้า", shard the tests), even when the user never says the word
  "standard".
---

# Fullstack CI/CD standard

An opinionated, production-paid-for way to ship a web + api project: GitHub Actions
builds everything, Cloudflare Pages serves the frontend, the VPS only pulls pre-built
images, one R2 bucket per org holds backups and blobs, and scheduled checks make
failures loud instead of silent. Every rule here exists because the opposite once
broke something real.

Work in exactly one of three modes — decide which before doing anything:

| The ask sounds like | Mode | Read |
|---|---|---|
| new repo going to production, "ตั้ง project ใหม่", set up CI/CD end to end | Greenfield setup | this file, then the references each phase points to |
| "ตรวจ/audit/review pipeline", "what's missing", "is this up to standard" | Audit | `references/verification.md` |
| merge/move buckets, rotate or rename tokens, consolidate environments | Migration | `references/r2-tokens.md` → Migration runbook |

## The end state

```
GitHub org (Free plan)
├─ web repo ── GH Actions gate → wrangler pages deploy
│                main → prod Pages project · development → dev project
│                any other branch → preview (<branch>.<project>.pages.dev)
│
├─ api repo ── gate (typecheck/lint/unit vs a real Postgres service)
│                → build image → hygiene check → GHCR (:sha-<commit> + :branch tags)
│                → VPS PULLS the pre-built image (never builds on the server)
│                deploy runs :sha-<commit>, never the branch tag
│                deploy order: pull → migrate (one-off run --rm) → up -d
│                              → poll /health → verify /version sha == commit
│                              → re-probe vs baseline → retag host :branch
│                → weekly GHCR prune (GITHUB_TOKEN) + trivy scan rides the same run
│
├─ R2 ──────── ONE bucket <org>-backup; environments are PREFIXES inside it
│                lifecycle: postgres/prod 365d · postgres/dev 30d · blobs 90d
│
├─ tokens ──── exactly two per org, Account API Tokens made in the dashboard:
│                <org>-backup-rw  R2 S3 token, Object Read & Write, that bucket only
│                <org>-pages      account API token, Cloudflare Pages: Edit
│
└─ backups ─── nightly VPS cron: pg_dump | gzip → local file + PUT to R2
                 (upload verified by remote size), fail-loud on any error
                 backup-health cron re-checks freshness (≤ 25h) every morning
```

Everything in the references exists to reach and hold this shape.

## Non-negotiable rules

Each rule's "why" is the compressed failure that paid for it.

1. **No build on the production host.** Dev and prod share one VPS; a build spike
   can OOM-kill the production stack. CI builds; the host pulls images.
2. **Migrate before the switch, never after `up -d`.** A one-off
   `docker compose run -T --rm <svc> migrate` runs between pull and up, so a
   failed migration ends the deploy before new code serves traffic.
3. **Every deploy verifies itself.** Backend: poll the service's own `/health`
   (not orchestrator container state), then compare `/version` sha against the
   commit — if the api doesn't expose these two endpoints, adding them is part
   of the setup, not an optional extra; the whole verification standard stands
   on them. Frontend: confirm the Pages deployment actually landed via
   `wrangler pages deployment list` (newest deployment matches the pushed
   branch). CI-green is not "deployed".
4. **The gate gates both branches, from one definition.** Free orgs cannot
   require checks, and main is reachable without a PR (direct push, UI edit,
   revert button) — so deploy.yml's `gate` job calls test.yml
   (`uses: ./.github/workflows/test.yml`, `on: workflow_call`). Never a second
   copy: a copy drifts and silently changes what gates a deploy. A slow gate
   gets sharded, never skipped: `references/cicd-pipeline.md` → Test gate speed.
   Inside the running gate, the pure checks may skip when a merged PR already
   passed Test on the identical tree: → Skip checks a merged PR already ran.
5. **Environments are prefixes, never buckets.** One bucket per org; dev/prod
   separation lives in the key prefix. Bucket-per-env once orphaned a token
   scope and uploads died silently for six weeks before anyone noticed.
6. **One of each credential per org, reused by all its repos.** Cloudflare:
   exactly two tokens, `<org>-backup-rw` for everything touching the bucket,
   `<org>-pages` for deploys (read/write separation traded away deliberately:
   one point to audit and revoke per type). CI: one Tailscale OAuth client
   (`github-actions-<org>-deploy`), one SSH deploy key, one GHCR `read:packages`
   PAT. A per-repo key turns the next repo into a new credential and every
   rotation into a hunt. Free private repos cannot read org-level secrets and
   values cannot be read back, so each repo holds its own copy, set in one
   loop and stored in the password manager at creation
   (`references/cicd-pipeline.md` → Secrets inventory). Temp tokens
   (migration, tunnel edit) carry an explicit expiry or get deleted when done.
7. **Create the two tokens in the dashboard**, as Account API Tokens
   (Manage account → Account API tokens), not user tokens, which die with the
   user. The API can make them too, but only with a token holding Account API
   Tokens Write, which can mint any token: keeping that around costs more than
   two clicks. If a token does come from `POST /accounts/{id}/tokens`, its S3
   pair is the token `id` and the SHA-256 of its `value`; the raw value as
   the secret fails every sigv4 call with SignatureDoesNotMatch
   (`references/r2-tokens.md` → Creating tokens).
8. **Lifecycle via `wrangler r2 bucket lifecycle add`, never a raw ruleset PUT.**
   The PUT replaces the whole ruleset and rejects rules without a transition.
   Always keep the default multipart-abort (7d) rule.
9. **`R2_KEY_PREFIX` is required whenever R2 is configured** — fail loud at
   boot. A missing prefix silently files one environment's files under the
   other's namespace.
10. **CORS before cutover for browser uploads.** Browser uploads are presigned
    PUTs straight to R2; a missing CORS rule fails as a network TypeError, not a
    403 — only a real browser test catches it. New bucket needs its CORS rule
    before traffic switches.
11. **Never delete an old bucket until a size-verified copy preserved history
    AND a scheduled backup cycle has landed in the new one.**
12. **Every job sets `timeout-minutes`** (tiered ~10/15/20 against real run
    times). The default 360-minute ceiling can drain the whole 2,000-minute
    free month in one hung run.
13. **Credentials never persist on the host.** Registry login goes through a
    temp `DOCKER_CONFIG` removed on exit, and only the pull step receives the
    credential; CI reaches the VPS over Tailscale with an ephemeral tag.
    `.env` stays hand-managed per environment.
14. **No inventory row, no credential.** Every bucket, token, key and secret
    is recorded before anything uses it, in one Hindsight document per org
    titled `Inventory: <org> CI/CD credentials` (`hindsight_ingest_document`).
    Re-ingest the whole table on every change: the newer document supersedes,
    so a partial ingest drops rows. Names, scopes, where each value lives and
    which repos hold a copy; never values (Hindsight is a server, anything
    sent stays). A temp token gets a row too, with its expiry, dropped when
    it is deleted. A project that already keeps an inventory file keeps it. The
    inventory is what catches dead orphans on cleanup passes.
15. **Tag the VPS tailnet node (`tag:<project>-vps`).** An untagged node's
    key expires and the host drops off the tailnet; with 22 open only on
    `tailscale0`, every SSH path dies with it. ACL, firewall and break-glass:
    `references/cicd-pipeline.md` → VPS access.
16. **Names follow what exists.** Before naming anything, read the sibling
    repos in the workset and the org's inventory. An existing name is reused
    exactly: renaming a compose project, volume, secret, bucket or token is a
    migration (data, deploys and backup scripts bind to it), not a cleanup. A
    new name takes the standard pattern with the full GitHub org name:
    `/srv/<org>/<repo>-<env>/`, compose project `<org>-<repo>-<env>`,
    `<org>-backup`, `<org>-backup-rw`, `<org>-pages`, secret names verbatim
    from the Secrets inventory table. Several orgs share one VPS and one
    Cloudflare account: a repo-only name like `api-dev` collides across orgs.

## Greenfield setup

Run the phases in order; each is done when its verify step passes. Read the
reference named at the start of a phase before acting in it.

**Phase 0 — prerequisites.** Confirm all of these exist before touching
anything; if one is missing, report the gap and stop rather than improvising
half a pipeline:
GitHub org (Free plan is assumed and sufficient) · one VPS shared by dev and
prod, its tailnet node tagged `tag:<project>-vps` (rule 15) · Tailscale with
an OAuth client able to tag `tag:ci` · a Cloudflare
account (Pages + R2) · two repos: `<org>/web` and `<org>/api`. Then list what
already exists: the org's inventory, `docker compose ls -a` and `/srv` on the
host, the org's existing CI credentials (rules 6 and 16 reuse them). Open
the inventory now: each credential created in any phase gets its row before
anything uses it (rule 14).

**Phase 1 — api pipeline.** Read `references/cicd-pipeline.md` (Backend
pipeline). Ends with: the api exposes `/health` and `/version` (build sha —
add them if missing), push to development deploys dev, both endpoints verify
the deploy, merge to main deploys prod the same way, each repo holds its own
copy of every secret it needs (Free private repos cannot read org-level
secrets; rule 6), and the CI reachability
probe passed (`references/verification.md` → VPS access probes).

**Phase 2 — web pipeline.** Read `references/cicd-pipeline.md` (Frontend
pipeline). The first deploy needs the `<org>-pages` token, so create it here
(`references/r2-tokens.md` → Creating tokens). Ends with: three Pages targets live (prod, dev, preview) behind the
gate job, and the deploy is verifiable via wrangler CLI — newest
`wrangler pages deployment list` row matches the push.

**Phase 3 — R2 + tokens.** Read `references/r2-tokens.md` (New-project setup).
Ends with: bucket + lifecycle rules verified, the S3 token created and stored
where the pipeline expects it, inventory re-ingested.

**Phase 4 — backups + health.** Read `references/cicd-pipeline.md` (Backups and
retention). Ends with: nightly cron produced a dump that is in R2 (size-verified)
and backup-health went green once.

**Phase 5 — close-out.** One restore drill: download last night's dump from R2,
restore into a scratch database, confirm it queries. A backup that has never
been restored is a hope, not a backup. Then confirm the inventory lists
every artifact created in phases 0–4.

## Audit

Read `references/verification.md` in full — it has the probe toolkit and the
report template. Two hard boundaries while auditing:

- Run **read-only** probes only (list / get / head / status checks). Any
  mutation — create, set, delete, rotate, or the CI reachability probe (it
  pushes a branch and runs Actions) — needs the user's explicit approval
  first; propose it as a finding instead of doing it.
- Never read or print secret values. Probe by name and by behaviour (a token
  that 200s its own bucket and 403s others is correctly scoped — no value
  needed); compare two copies by sha256 prefix. A sed "redaction" of a
  secrets file once printed an R2 key into the log.

Emit the compliance report in the template from verification.md: one row per
check — expected, found, verdict, fix.

## Migration

Read `references/r2-tokens.md` → Migration runbook before proposing anything.
The cutover ORDER is load-bearing; out of order it produces wrongly-prefixed
objects no lifecycle covers, or a crash-loop window, or data loss. Highlights:
deploy the new script before flipping the backup env; pre-flip the app env
before promote; re-run the copy to catch stragglers; delete old buckets and
tokens only after a scheduled backup lands in the new bucket.
