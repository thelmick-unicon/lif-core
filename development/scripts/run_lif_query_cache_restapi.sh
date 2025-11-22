#!/bin/bash
uv run uvicorn lif.query_cache_restapi.core:app --host 0.0.0.0 --port 8001
