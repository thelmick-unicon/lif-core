#!/bin/bash
echo "Waiting for Postgres ( $POSTGRES_HOST:$POSTGRES_PORT@$POSTGRES_USER for database $POSTGRES_DB ) to be ready..."
until pg_isready --host=$POSTGRES_HOST --port=$POSTGRES_PORT --username=$POSTGRES_USER --dbname=$POSTGRES_DB; do
sleep 2
done
echo "Restoring SQL backup to $POSTGRES_HOST:$POSTGRES_PORT@$POSTGRES_USER for database $POSTGRES_DB..."
psql --host=$POSTGRES_HOST --port=$POSTGRES_PORT --username=$POSTGRES_USER --dbname=$POSTGRES_DB -f /backup.sql
echo 'SQL Backup restored successfully!'
# echo 'Waiting for Postgres to be ready...'
# until pg_isready --host=$POSTGRES_HOST --username=$POSTGRES_USER --dbname=$POSTGRES_DB; do
#   sleep 2
# done
# pg_restore -l /backup.tar
# echo 'Restoring backup...'
# pg_restore --host=$POSTGRES_HOST --username=$POSTGRES_USER --dbname=$POSTGRES_DB --clean -F c /backup.tar
# echo 'Backup restored successfully!'
