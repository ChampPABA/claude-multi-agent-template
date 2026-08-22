# Cloudflare inventory — acme

| artifact | type | scope |
|---|---|---|
| acme-prod-backup | bucket | prod DB backups |
| acme-dev-backup | bucket | dev DB backups |
| acme-old-backup | bucket | leftover from the 2025 migration, believed empty |
| acme-full-rw | R2 S3 token | Object Read & Write, all buckets in the account |
