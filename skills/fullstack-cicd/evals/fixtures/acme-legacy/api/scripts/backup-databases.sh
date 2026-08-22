#!/bin/bash
# Nightly backups — crontab 03:30, output to backup.log
BACKUP_DIR="$HOME/backups"
DATE=$(date +%Y%m%d_%H%M%S)

for spec in acme_prod_db:postgres:acme_prod acme_dev_db:postgres:acme_dev; do
  IFS=: read -r container user db <<<"$spec"
  docker exec "$container" pg_dump -U "$user" "$db" | gzip > "$BACKUP_DIR/${db}_$DATE.sql.gz"
  . "$BACKUP_DIR/.r2.env"
  curl -s -o /dev/null --aws-sigv4 "aws:amz:auto:s3" \
    --user "$R2_ACCESS_KEY_ID:$R2_SECRET_ACCESS_KEY" \
    -T "$BACKUP_DIR/${db}_$DATE.sql.gz" \
    "$R2_ENDPOINT/$R2_BUCKET/${db}_$DATE.sql.gz" || true
done

echo "Backup done: $DATE"
