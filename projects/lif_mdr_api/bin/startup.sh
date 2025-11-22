#!/bin/sh
# alembic upgrade head
cd ..
uvicorn lif.mdr_restapi.core:app --workers 1 --host 0.0.0.0 --port 8012 --log-level debug
