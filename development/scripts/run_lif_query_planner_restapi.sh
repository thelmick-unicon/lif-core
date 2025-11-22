#!/bin/bash
uv run uvicorn lif.query_planner_restapi.core:app --host 0.0.0.0 --port 8002 --timeout-keep-alive 30
