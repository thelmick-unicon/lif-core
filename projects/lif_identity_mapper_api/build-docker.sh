#!/bin/bash

set -e

# Configuration
IMAGE_TAG=${1:-lif-identity-mapper}
PROJ_DIR=${2:-lif_identity_mapper_api}

# Change to repo root
cd "$(dirname "$0")/../.."

echo "Building ${IMAGE_TAG} from repo root..."
docker build -f projects/${PROJ_DIR}/Dockerfile2 -t ${IMAGE_TAG} .

echo "Build complete!"
