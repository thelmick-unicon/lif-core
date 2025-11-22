#!/bin/bash

set -e

# Configuration
IMAGE_TAG=${1:-lif-orchestrator-api}
PROJ_DIR=${2:-lif_orchestrator_api}

# Change to repo root
cd "$(dirname "$0")/../.."
echo "Building ${IMAGE_TAG} from repo root..."
docker build -f projects/${PROJ_DIR}/Dockerfile2 -t ${IMAGE_TAG} .

echo "Build complete!"