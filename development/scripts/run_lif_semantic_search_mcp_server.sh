#!/bin/bash
export LIF_GRAPHQL_ROOT_NODE=Person
export LIF_GRAPHQL_API_URL=http://localhost:8000/graphql
export OPENAPI_JSON_FILENAME=openapi_constrained_with_interactions.json

# Keeping the original command for reference:
# uv run fastmcp run --transport http --host 0.0.0.0 --port 8003 ../../bases/lif/semantic_search_mcp_server/core.py:mcp

uv run uvicorn lif.semantic_search_mcp_server.core:http_app --host 0.0.0.0 --port 8003
