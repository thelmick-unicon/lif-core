#!/usr/bin/env bash
set -euo pipefail

# run_graphql_query.sh
# Usage: run_graphql_query.sh -e ENDPOINT_URL [-k API_KEY] [-t BEARER_TOKEN] [-i IDENTIFIER]
#
# This script POSTs a GraphQL query to an endpoint and allows overriding the identifier.
#
# This script can be called from Cloudshell with private VPC access in order
# to test a graphql query on the ECS cluster. Use s3 cp to copy this script
# to the Cloudshell environment.

ENDPOINT_URL="http://graphql-org1.lif.dev.aws:8000/graphql"
API_KEY=""
BEARER_TOKEN=""
IDENTIFIER=""
VERBOSE=0

log() { printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >&2; }

usage() {
  cat <<EOF
Usage: $0 [-e ENDPOINT_URL] [-k API_KEY] [-t BEARER_TOKEN] [-i IDENTIFIER] [-v]

Options:
  -e ENDPOINT_URL   GraphQL HTTP(S) endpoint (default: http://graphql-org1.lif.dev.aws:8000/graphql)
  -k API_KEY        Optional API key to send as 'x-api-key' header
  -t BEARER_TOKEN   Optional Bearer token to send as 'Authorization: Bearer <token>'
  -i IDENTIFIER     Identifier to use in the GraphQL filter (required)
  -v                Verbose output (show request/response headers)

Example:
  $0 -e https://your-ecs-endpoint/graphql -i 200002 -k myapikey
  aws s3 cp s3://my-bucket/run_graphql_query.sh - | bash -s -- -i 200002 -e https://your-ecs-endpoint/graphql -k MY_API_KEY
EOF
}

while getopts ":e:k:t:i:vh" opt; do
  case "$opt" in
    e) ENDPOINT_URL="$OPTARG" ;;
    k) API_KEY="$OPTARG" ;;
    t) BEARER_TOKEN="$OPTARG" ;;
  i) IDENTIFIER="$OPTARG" ;;
    v) VERBOSE=1 ;;
    h) usage; exit 0 ;;
    :) echo "Option -$OPTARG requires an argument." >&2; usage; exit 2 ;;
    \?) echo "Invalid option: -$OPTARG" >&2; usage; exit 2 ;;
  esac
done

# Identifier is required
if [ -z "$IDENTIFIER" ]; then
  echo "ERROR: -i IDENTIFIER is required" >&2
  usage
  exit 2
fi

# The GraphQL query template. IDENTIFIER will be interpolated.
GRAPHQL_QUERY_TEMPLATE=$(cat <<'GRAPHQL'
query MyQuery {
  person(
    filter: {identifier: {identifier: "%IDENTIFIER%", identifierType: SCHOOL_ASSIGNED_NUMBER}}
  ) {
    name {
      firstName
      lastName
    }
  }
}
GRAPHQL
)

# Substitute identifier into the query
GRAPHQL_QUERY=${GRAPHQL_QUERY_TEMPLATE//%IDENTIFIER%/$IDENTIFIER}

# Create temp files (portable mktemp usage)
TMPDIR_DEFAULT=${TMPDIR:-/tmp}
TMP_BODY=$(mktemp "${TMPDIR_DEFAULT%/}/run_graphql.XXXXXX")
TMP_HDR=$(mktemp "${TMPDIR_DEFAULT%/}/run_graphql.hdr.XXXXXX")
TMP_OUT=$(mktemp "${TMPDIR_DEFAULT%/}/run_graphql.out.XXXXXX")
TMP_CODE=$(mktemp "${TMPDIR_DEFAULT%/}/run_graphql.code.XXXXXX")

cleanup() {
  rm -f "$TMP_BODY" "$TMP_HDR" "$TMP_OUT" "$TMP_CODE" 2>/dev/null || true
}
trap cleanup EXIT

# Encode JSON safely using python3 or python; use stdin to avoid quoting issues
if command -v python3 >/dev/null 2>&1; then
  printf '%s' "$GRAPHQL_QUERY" | python3 -c 'import sys,json; print(json.dumps({"query": sys.stdin.read()}))' >"$TMP_BODY"
elif command -v python >/dev/null 2>&1; then
  printf '%s' "$GRAPHQL_QUERY" | python -c 'import sys,json; print(json.dumps({"query": sys.stdin.read()}))' >"$TMP_BODY"
else
  echo "ERROR: python3 or python is required to JSON-encode the GraphQL query." >&2
  rm -f "$TMP_BODY" 2>/dev/null || true
  exit 2
fi

if [ "$VERBOSE" -eq 1 ]; then
  log "Endpoint: $ENDPOINT_URL"
  log "Identifier: $IDENTIFIER"
  command -v curl >/dev/null 2>&1 && log "curl: $(curl --version | head -n1)" || log "curl not found"
  command -v python3 >/dev/null 2>&1 && log "python3: $(python3 --version 2>&1)" || true
  command -v python >/dev/null 2>&1 && log "python: $(python --version 2>&1)" || true
  command -v jq >/dev/null 2>&1 && log "jq: $(jq --version 2>/dev/null)" || log "jq not found (output will be raw)"
  log "Request JSON file: $TMP_BODY ($(wc -c <"$TMP_BODY" 2>/dev/null || echo 0) bytes)"
fi

# Build curl arguments
CURL_ARGS=(--silent --show-error -X POST "$ENDPOINT_URL" -H "Content-Type: application/json" --data-binary "@$TMP_BODY")
if [ -n "$API_KEY" ]; then
  CURL_ARGS+=( -H "x-api-key: $API_KEY" )
fi
if [ -n "$BEARER_TOKEN" ]; then
  CURL_ARGS+=( -H "Authorization: Bearer $BEARER_TOKEN" )
fi
STATUS=""

if [ "$VERBOSE" -eq 1 ]; then
  # Shell trace in verbose mode to surface early failures
  set -x
  log "Posting GraphQL query to: $ENDPOINT_URL"
  # Show first line of JSON to avoid huge logs, and total bytes printed above
  head -n1 "$TMP_BODY" >&2 || true
fi

# Perform request: write headers to TMP_HDR, body to TMP_OUT, capture HTTP status
EXTRA_CURL=()
if [ "$VERBOSE" -eq 1 ]; then EXTRA_CURL+=( --verbose ); fi
set +e
curl -D "$TMP_HDR" -o "$TMP_OUT" -w '%{http_code}' "${EXTRA_CURL[@]}" "${CURL_ARGS[@]}" \
  1>"$TMP_CODE" \
  2> >(if [ "$VERBOSE" -eq 1 ]; then tee /dev/stderr; else cat 1>&2; fi)
CURL_EXIT=$?
STATUS=$(tr -d '\n' <"$TMP_CODE")
set -e
if [ "$VERBOSE" -eq 1 ]; then
  log "curl exit code: $CURL_EXIT"
  # Show headers and file sizes only in verbose mode
  log "HTTP status: ${STATUS:-<none>}"
  log "Header file size: $(wc -c <"$TMP_HDR" 2>/dev/null || echo 0) bytes"
  log "Body file size: $(wc -c <"$TMP_OUT" 2>/dev/null || echo 0) bytes"
  echo "--- Response headers ---" >&2
  sed $'s/\r$//' "$TMP_HDR" >&2 || true
  echo "------------------------" >&2
fi

# Print body (pretty if jq available)
if command -v jq >/dev/null 2>&1; then
  if jq . >/dev/null 2>&1 <"$TMP_OUT"; then
    jq . <"$TMP_OUT"
  else
    # Not valid JSON; print raw
    cat "$TMP_OUT"
  fi
else
  cat "$TMP_OUT"
fi

# Non-2xx statuses or curl failures should cause a non-zero exit code
if [ "$CURL_EXIT" -ne 0 ]; then
  # Print concise error even when not verbose
  echo "ERROR: curl failed with exit code $CURL_EXIT" >&2
  exit "$CURL_EXIT"
fi
case "$STATUS" in
  2*) exit 0 ;;
  *) echo "ERROR: Request completed with HTTP status ${STATUS:-<none>}" >&2; exit 3 ;;
esac

exit 0
