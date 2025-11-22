#!/bin/bash

# This script builds wheels for all polylith projects in the projects directory.
# It assumes that each project has a build.sh script in its root directory.

set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PROJECTS_DIR="$ROOT_DIR/projects"

for project_dir in "$PROJECTS_DIR"/*/; do
    if [ -f "$project_dir/build.sh" ]; then
        echo "Building wheel in $project_dir"
        (cd "$project_dir" && bash build.sh)
    else
        echo "No build.sh found in $project_dir, skipping."
    fi
done