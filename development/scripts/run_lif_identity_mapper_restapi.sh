#!/bin/bash
uv run uvicorn lif.identity_mapper_restapi.core:app --host 0.0.0.0 --port 8006 --timeout-keep-alive 30
