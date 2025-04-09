#!/bin/sh

# Stop script execution at error
set -e

# Check env variables aren't missing
if [ -z "${DATABASE_BUCKET}" ]; then
  echo "$(date) - missing DATABASE_BUCKET environment variable."
  exit 1
fi

# Compile script variables
PGDB=${DATABASE_NAME:-postgres}
PGUSER=${DATABASE_USER:-postgres}
PGHOST=${DATABASE_HOST:-localhost}
PGPORT=${DATABASE_PORT:-5432}
PGIGNORE_TABLE=${DATABASE_BACKUP_IGNORE_TABLE_REGEX:-""}
PGIGNORE_CONTENT=${DATABASE_BACKUP_IGNORE_CONTENT_REGEX:-""}
# https://www.postgresql.org/docs/10/libpq-envars.html
export PGPASSWORD=$DATABASE_PASSWORD

case "$1" in

    backup-to-s3)
        echo "$(date) - dumping ${PGDB} from host: ${PGHOST}"
        DATE_SUFFIX="$(date +%Y-%m-%d)"
        set -- "$@" -d $PGDB -p $PGPORT -U $PGUSER -h $PGHOST
        set -- "$@" --exclude-table=$PGIGNORE_TABLE
        set -- "$@" --exclude-table-data=$PGIGNORE_CONTENT

        # Compressed plain SQL backup, to use with psql -f
        TMP_FILE="${DATE_SUFFIX}.sql.gz"
        pg_dump "$@" | gzip > $TMP_FILE

        # Custom-format binary backup, to use with pg_restore
        TMP_BACKUP_FILE="${DATE_SUFFIX}.dump"
        pg_dump -Fc "$@" -f $TMP_BACKUP_FILE

        echo "$(date) - uploading file ${TMP_FILE} to ${DATABASE_BUCKET}"
        S3_URL="s3://${DATABASE_BUCKET}/${TMP_FILE}"
        aws s3 cp $TMP_FILE $S3_URL > /dev/null

        echo "$(date) - uploading file ${TMP_BACKUP_FILE} to ${DATABASE_BUCKET}"
        S3_URL="s3://${DATABASE_BUCKET}/${TMP_BACKUP_FILE}"
        aws s3 cp $TMP_BACKUP_FILE $S3_URL > /dev/null
        ;;

    *)
        echo "$(date) - executing shell command: $@"
        exec "$@"
        ;;

esac
