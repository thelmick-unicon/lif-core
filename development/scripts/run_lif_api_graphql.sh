#!/bin/bash
export LIF_QUERY_PLANNER_URL=http://localhost:8002

uv run uvicorn lif.api_graphql.core:app --host 0.0.0.0 --port 8000
