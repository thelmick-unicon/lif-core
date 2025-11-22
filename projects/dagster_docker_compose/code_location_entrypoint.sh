#!/bin/bash
# This script makes it simpler to pass environment variables to a Dagster job run
# when using the DockerRunLauncher in a Docker Compose setup.
# See: https://github.com/dagster-io/dagster/discussions/21100#discussioncomment-10999238

# Load environment variables that start with ADAPTERS__, LIF_, or USER_CODE_ from the host environment
env_vars=$(env | grep -E '^(ADAPTERS__|LIF_|USER_CODE_)' | xargs -I{} echo \"{}\" | paste -sd, - )

dagster code-server start -p 4000 -h 0.0.0.0 -m lif_orchestrator.definitions --container-context="{\"env_vars\": [$env_vars]}"
