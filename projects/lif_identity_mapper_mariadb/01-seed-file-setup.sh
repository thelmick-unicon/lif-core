#!/bin/bash
set -e

# Wait for MariaDB to start
echo "EP: Waiting for MariaDB to start..."
sleep 5

# If SEED_DATA_KEY is not set, then skip the import of the seed data
if [ -z "${SEED_DATA_KEY}" ]; then
  echo "EP: SEED_DATA_KEY is not set. Skipping seed data import."
  exit 0
fi

# Get SEED_DATA_KEY from environment variable
echo "EP: Using seed data key: $SEED_DATA_KEY"

# Validate SEED_DATA_KEY to prevent path traversal and shell injection
if ! [[ "$SEED_DATA_KEY" =~ ^[a-zA-Z0-9_-]+$ ]]; then
  echo "EP: Invalid SEED_DATA_KEY value. Only alphanumeric, underscore, and hyphen are allowed."
  exit 1
fi

# Copy seed file to location where it will automatically get picked up
echo "EP: Copying seed file /seed_data/$SEED_DATA_KEY/seed.sql to /docker-entrypoint-initdb.d/03-seed.sql"
cat /seed_data/${SEED_DATA_KEY}/seed.sql > /docker-entrypoint-initdb.d/03-seed.sql
