# acme

GitHub org `acme` on the Free plan. One VPS shared by dev and prod
(`/srv/acme-dev`, `/srv/acme-prod`), reached over Tailscale. Cloudflare
account with R2 + Pages (single Pages project `acme-web`).

Nightly backup cron (03:30 on the VPS) runs
`api/scripts/backup-databases.sh`; logs to `~/backups/backup.log`.

Repos: `acme/web` (Vite frontend), `acme/api` (Elysia + Postgres).
