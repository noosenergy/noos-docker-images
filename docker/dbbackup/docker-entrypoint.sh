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
PGIGNORE=${DATABASE_BACKUP_IGNORE_REGEX:-""}
# https://www.postgresql.org/docs/10/libpq-envars.html
export PGPASSWORD=$DATABASE_PASSWORD

case "$1" in

    backup-to-s3)
        echo "$(date) - dumping ${PGDB} from host: ${PGHOST}"
        TMP_FILE="$(date +%Y-%m-%d).sql.gz"
        pg_dump -d $PGDB -p $PGPORT -U $PGUSER -h $PGHOST --exclude-table-data=$PGIGNORE -- | gzip > $TMP_FILE

        echo "$(date) - uploading file ${TMP_FILE} to ${DATABASE_BUCKET}"
        S3_URL="s3://${DATABASE_BUCKET}/${TMP_FILE}"
        aws s3 cp $TMP_FILE $S3_URL > /dev/null
        ;;

    *)
        echo "$(date) - executing shell command: $@"
        exec "$@"
        ;;

esac
