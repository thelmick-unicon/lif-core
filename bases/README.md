
# `bases/` Directory

This directory defines the **deployment contexts** for the system’s modular components. In a [Polylith](https://polylith.gitbook.io/polylith) architecture, `bases/` houses the concrete Python applications or services that assemble and deploy functionality from the reusable `components/` layer.

## Purpose

Each base is a fully functional deployment unit — such as a REST API, GraphQL endpoint, or serverless handler — that integrates and composes logic from multiple components. These bases do **not** define core business logic; instead, they **wrap components** to expose them via specific runtime environments.

This aligns with Polylith’s goal of maximizing reuse while keeping deployment boundaries clean and explicit.

---

## Directory Structure

Each subdirectory within `bases/` is a Python module that defines a single deployable target. For example:

<pre lang="markdown"> <code> 
bases/
│
├── lif/
│ ├── api_graphql/ # GraphQL service base
│ │ ├── init.py
│ │ └── core.py
│ │
│ ├── advisor_restapi/ # REST API for Advisor service
│ ├── query_cache_restapi/ # REST API for cached queries
│ ├── semantic_search_mcp_server/ # Semantic search MCP server
│ ├── query_planner_restapi/ # Query planner API
│ └── query_cache_module/ # Query cache runtime module    
</code> </pre>


Each of these follows a similar structure:
- `__init__.py` — Initializes the module
- `core.py` — Entrypoint logic: sets up routes, connects to components, configures context, etc.

---

## Example: How Bases Work

    bases/lif/query_cache_restapi/core.py
    
    from components.query_cache import cache_service
    from fastapi import FastAPI
    
    app = FastAPI()
    
    @app.get("/cache")
    def read_cache(key: str):
        return cache_service.get(key)

This shows how a base integrates a component and exposes it via a web API.

## Testing
Tests for these deployment contexts should be lightweight and focused on:

 - Correct integration of components
 - Input/output interface behavior (e.g. HTTP routes)
 - Configuration or startup scripts

## Conventions

 - Avoid business logic inside bases — push that to components.
 - Keep `core.py` focused on orchestration and infrastructure glue.
 - Use environment variables or config files for deployment-specific settings.

## Releated Folders
 - [components/](../components/): where reusable business logic and services are defined.
 - [projects/](../projects/): can be used to group bases/components into deployable systems.

## Further Reading
-   [Polylith Architecture Docs](https://polylith.gitbook.io)
-   [Polylith for Python (Concept)](https://github.com/polylith/polylith#readme)
