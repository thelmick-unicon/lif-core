
# `development/` Directory 

The `development/` directory supports local development workflows and tooling for this Polylith-based Python monorepo.

In a Polylith architecture, the `development/` directory is the designated space for developer-centric tools, utilities, and configurations. These assets facilitate the building, testing, running, and debugging of the system's components and projects — without introducing deployment-specific configuration or runtime state.

## Purpose

- Provide shell scripts and automation for running services and APIs locally
- House development-only Dockerfiles, Compose configurations, or mock data
- Enable a reproducible and fast development environment
- Serve as a workspace for rapid testing of individual bricks (components, bases, projects)

## Typical Contents

The structure may vary over time, but commonly includes:

<pre lang="markdown"> <code> 
development/  
├── docker-compose.yml # Spin up local infrastructure (e.g., MongoDB)  
├── patrick/ # Local test data and mock records  
│ ├── load_mongodb.sh  
│ └── six_lif_validated_records_array.json  
├── mcp_client/ # Dev/test clients for MCP interfaces  
│ └── client.py  
├── mongodb/ # Docker setup for local MongoDB  
│ └── Dockerfile  
├── scripts/ # Utilities to run and build services  
│ ├── run_lif_api_graphql.sh  
│ ├── run_lif_query_planner_restapi.sh  
│ ├── run_lif_query_cache_restapi.sh  
│ ├── run_lif_semantic_search_mcp_server.sh  
│ ├── run_lif_advisor_restapi.sh  
│ ├── run_docker_mongodb.sh  
│ ├── build_all_project_wheels.sh  
│ └── graphql/  
│ └── write_out_schema.py
</code> </pre>


## Usage Examples

To start MongoDB locally via Docker:
`bash development/scripts/run_docker_mongodb.sh`

To run a specific API service in a local environment:
`bash development/scripts/run_lif_advisor_restapi.sh`

To load test data into a development database:
`bash development/patrick/load_mongodb.sh`

## Guidelines

-   The code and scripts in this directory are intended **only for local development** — not for production or deployment use.
-   Keep logic modular and decoupled from real infrastructure when possible (e.g., use mocks or stubs).
-   Use this space to add temporary utilities or iterate quickly on experiments.
-   Prefer scripting in a consistent language (e.g., Bash, Python) and use appropriate shebangs and permission flags for executable scripts.

## Related Context

-   [Polylith Architecture Docs](https://polylith.gitbook.io)
-   [bases/](../bases/) — defines how components are deployed
-   [components/](../components/) — reusable building blocks of the system
