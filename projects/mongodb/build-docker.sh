#!/bin/bash

set -e

# Configuration
IMAGE_TAG=${1:-mongodb}
PROJ_DIR=${2:-mongodb}

# Change to repo root
#cd "$(dirname "$0")/../.."

#echo "Building ${IMAGE_TAG} from repo root..."
#docker build -f projects/${PROJ_DIR}/Dockerfile -t ${IMAGE_TAG} .
echo "Building ${IMAGE_TAG} from project root..."
docker build -t ${IMAGE_TAG} .

echo "Build complete!"
