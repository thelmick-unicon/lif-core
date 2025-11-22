#!/bin/bash
set -e

# Wait for Mongo to start
echo "EP: Waiting for MongoDB to start..."
sleep 5

# If SEED_DATA_KEY is not set, then skip the import of the seed data
if [ -z "${SEED_DATA_KEY}" ]; then
  echo "EP: SEED_DATA_KEY is not set. Skipping seed data import."
  exit 0
fi

# Get SEED_DATA_KEY from environment variable
echo "EP: Using seed data key: $SEED_DATA_KEY"

# Combine JSON arrays from all files matching *.json
echo "EP: Combining all JSON files in /seed_data/$SEED_DATA_KEY/"
jq -s . /seed_data/${SEED_DATA_KEY}/*.json > /seed-data.json

# Import into MongoDB
echo "EP: Importing data into $MONGO_DB.$MONGO_COLLECTION at $MONGO_HOST..."
mongoimport \
  --db "$MONGO_DB" \
  --collection "$MONGO_COLLECTION" \
  --type json \
  --drop \
  --file /seed-data.json \
  --jsonArray
