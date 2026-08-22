---
name: fullstack-cicd
description: >-
  End-to-end standard for standing up, extending, or auditing a full-stack project's
  infrastructure: GitHub Actions CI/CD on the Free org plan, Cloudflare Pages frontend
  deploys, GHCR + VPS immutable-image backend deploys, one R2 bucket per org with
  lifecycle rules, exactly two Cloudflare tokens (dashboard-only), and nightly database
  backups with health-check crons. Use whenever the task is setting up a new project's
  pipeline from scratch ("set up CI/CD", "ตั้ง project ใหม่", "deploy หน้าบ้านหลังบ้านให้ครบ"),
  adding R2 storage or backups, creating or rotating Cloudflare tokens, migrating or
  consolidating R2 buckets, or auditing an existing project against this standard
  ("ตรวจว่า pipeline ครบไหม", "what am I missing to deploy properly"). Also use for any
  question touching R2 buckets, R2 S3 tokens, Pages API tokens, wrangler r2
  lifecycle/cors, GHCR retention, or deploy-pipeline shape, even when the user never
  says the word "standard".
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
│                any other branch → preview (<branch>.pages.dev)
│
├─ api repo ── gate (typecheck/lint/unit vs a real Postgres service)
│                → build image → GHCR (:sha-<commit> + :branch tags)
│                → VPS PULLS the pre-built image (never builds on the server)
│                deploy order: pull → migrate (one-off run --rm) → up -d
│                              → poll /health → verify /version sha == commit
│                → weekly GHCR prune + trivy scan rides the same run
│
├─ R2 ──────── ONE bucket <org>-backup; environments are PREFIXES inside it
│                lifecycle: postgres/prod 365d · postgres/dev 30d · blobs 90d
│
├─ tokens ──── exactly two per org, both created in the DASHBOARD:
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
4. **The gate gates both branches.** Free orgs cannot require checks, and main is
   reachable without a PR (direct push, UI edit, revert button) — so the
   typecheck/lint/test job is duplicated inside deploy.yml. Keep it in step with
   test.yml's copy.
5. **Environments are prefixes, never buckets.** One bucket per org; dev/prod
   separation lives in the key prefix. Bucket-per-env once orphaned a token
   scope and uploads died silently for six weeks before anyone noticed.
6. **Exactly two tokens per org.** `<org>-backup-rw` for everything touching the
   bucket, `<org>-pages` for deploys. Read/write separation is traded away
   deliberately (one point to audit and revoke per type).
7. **R2 S3 tokens and Pages tokens can only be created in the dashboard.** The
   API's `POST /accounts/{id}/tokens` returns a bearer value that does not sign
   S3 requests (SignatureDoesNotMatch), and the API has no Pages permission
   group. Budget the two dashboard clicks; everything else is CLI-able.
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
    temp `DOCKER_CONFIG` removed on exit; CI reaches the VPS over Tailscale
    with an ephemeral tag. `.env` stays hand-managed per environment.
14. **No inventory row, no token.** Every bucket and token is recorded in the
    project's inventory doc (names, scopes, where each credential lives —
    never the values) before anything uses it. This rule is what catches
    dead orphans on cleanup passes.

## Greenfield setup

Run the phases in order; each is done when its verify step passes. Read the
reference named at the start of a phase before acting in it.

**Phase 0 — prerequisites.** Confirm all of these exist before touching
anything; if one is missing, report the gap and stop rather than improvising
half a pipeline:
GitHub org (Free plan is assumed and sufficient) · one VPS shared by dev and
prod · Tailscale with an OAuth client able to tag `tag:ci` · a Cloudflare
account (Pages + R2) · two repos: `<org>/web` and `<org>/api`.

**Phase 1 — api pipeline.** Read `references/cicd-pipeline.md` (Backend
pipeline). Ends with: the api exposes `/health` and `/version` (build sha —
add them if missing), push to development deploys dev, both endpoints verify
the deploy, merge to main deploys prod the same way.

**Phase 2 — web pipeline.** Read `references/cicd-pipeline.md` (Frontend
pipeline). Ends with: three Pages targets live (prod, dev, preview) behind the
gate job, and the deploy is verifiable via wrangler CLI — newest
`wrangler pages deployment list` row matches the push.

**Phase 3 — R2 + tokens.** Read `references/r2-tokens.md` (New-project setup).
Ends with: bucket + lifecycle rules verified, both tokens created and stored
where the pipeline expects them, inventory row written.

**Phase 4 — backups + health.** Read `references/cicd-pipeline.md` (Backups and
retention). Ends with: nightly cron produced a dump that is in R2 (size-verified)
and backup-health went green once.

**Phase 5 — close-out.** One restore drill: download last night's dump from R2,
restore into a scratch database, confirm it queries. A backup that has never
been restored is a hope, not a backup. Then confirm the inventory doc lists
every artifact created in phases 0–4.

## Audit

Read `references/verification.md` in full — it has the probe toolkit and the
report template. Two hard boundaries while auditing:

- Run **read-only** probes only (list / get / head / status checks). Any
  mutation — create, set, delete, rotate — needs the user's explicit approval
  first; propose it as a finding instead of doing it.
- Never read or print secret values. Probe by name and by behaviour (a token
  that 200s its own bucket and 403s others is correctly scoped — no value
  needed).

Emit the compliance report in the template from verification.md: one row per
check — expected, found, verdict, fix.

## Migration

Read `references/r2-tokens.md` → Migration runbook before proposing anything.
The cutover ORDER is load-bearing; out of order it produces wrongly-prefixed
objects no lifecycle covers, or a crash-loop window, or data loss. Highlights:
deploy the new script before flipping the backup env; pre-flip the app env
before promote; re-run the copy to catch stragglers; delete old buckets and
tokens only after a scheduled backup lands in the new bucket.
