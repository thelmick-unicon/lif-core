#!/bin/bash

# -------- CONFIG ---------
DB_NAME="LIF"
COLLECTION_NAME="person"
# JSON_FILE="$HOME/lif_mcp_demo/validated.json"
JSON_FILE="six_lif_validated_records_array.json"
MONGO_URI="mongodb://localhost:27017"
USE_JSON_ARRAY=true   # Set to true if file is a JSON array
# -------------------------

# Check for mongoimport
if ! command -v mongoimport &> /dev/null; then
  echo "❌ mongoimport not found. Installing..."
  sudo apt update
  sudo apt install -y mongodb-database-tools
fi

# Expand ~ manually if used
JSON_FILE_EXPANDED=$(eval echo "$JSON_FILE")

# Check file exists
if [ ! -f "$JSON_FILE_EXPANDED" ]; then
  echo "❌ JSON file '$JSON_FILE_EXPANDED' not found."
  exit 1
fi

echo "📤 Importing '$JSON_FILE_EXPANDED' into MongoDB collection '$COLLECTION_NAME'..."

# Build command
CMD="mongoimport --uri=\"$MONGO_URI\" --db=\"$DB_NAME\" --collection=\"$COLLECTION_NAME\" --file=\"$JSON_FILE_EXPANDED\""

if [ "$USE_JSON_ARRAY" = true ]; then
  CMD="$CMD --jsonArray"
fi

# Run and check success
echo "▶️ Running: $CMD"
if eval $CMD; then
  echo "✅ Import complete!"
else
  echo "❌ Import failed. Check syntax and file content."
  exit 1
fi

# Post-import tip
echo "ℹ️ To verify:"
echo "   mongosh --eval 'db.getSiblingDB(\"LIF\").person.find().forEach(doc => printjson(doc))'"
