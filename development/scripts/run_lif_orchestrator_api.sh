#!/bin/bash
export LIF_QUERY_PLANNER_URL=http://localhost:8002

uv run uvicorn lif.orchestrator_restapi.core:app --host 0.0.0.0 --port 8005
