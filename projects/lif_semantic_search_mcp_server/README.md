# Example usage

## Build the project
Navigate to this folder (where the `pyproject.toml` file is)

1. Export the dependencies (when using uv workspaces and having no project-specific lock-file):
``` shell
uv export --no-emit-project --output-file requirements.txt
```

2. Build a wheel:
``` shell
uv build --out-dir ./dist
```

## Build a docker image

``` shell
./build-docker.sh
```

## Run the image

``` shell
docker run -d --name lif_semantic_search_mcp_server -p 8003:8003 -e LIF_GRAPHQL_ROOT_NODE=Person -e LIF_QUERY_PLANNER_URL=http://host.docker.internal:8002 lif_semantic_search_mcp_server
```

The MCP server can now be accessed at http://localhost:8003/mcp. There is no UI, so the mcp server
should be accessed with a FastMCP client (see development/mcp_client/client.py for development).

## MDR Integration

Currently there is no direct MDR integration for this service. It was decided that the Semantic Search would just pull from the static file for now because of:
1) Time constraints and possible need for code refactor
2) Future features that may handle some of the refactor and have some overlap

Semantic Search still uses the `mdr_client` component to access the static OpenAPI LIF Data Model file.
