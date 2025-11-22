
# `components/` Directory

This directory contains the **reusable building blocks** — or _bricks_ — of your system. In [Polylith architecture](https://polylith.gitbook.io), components encapsulate distinct **features, services, or utilities** that can be composed together to build deployable applications (defined in the [`bases/`](../bases/) directory).

Each component is a **self-contained Python module** exposing core functionality, like services, features or utilities, that can be reused across multiple deployment contexts.

## Purpose

Components represent your system’s domain logic, integrations, or utility services. For example:
- `query_cache_service/` – Handles cache logic
- `openapi_to_graphql/` – Transforms OpenAPI schemas to GraphQL
- `semantic_search_service/` – Encapsulates semantic search functionality

Components should be:
 - Purely logical (no deployment code)
 - Fully testable in isolation

## Structure Overview

Each component lives in its own directory with a standard layout:

<pre lang="markdown"> <code> 
components/  
│  
├── lif/  
│ ├── query_cache_service/ # Caching service  
│ │ ├── **init**.py  
│ │ └── core.py  
│ │  
│ ├── openapi_to_graphql/ # Schema converter  
│ │ ├── core.py  
│ │ ├── type_factory.py  
│ │ └── schema_tools.py  
│ │  
│ ├── query_cache_read_store_mongodb/ # MongoDB cache read layer  
│ ├── openapi_schema_parser/ # OpenAPI parser  
│ ├── semantic_search_service/ # Semantic search logic  
│ ├── auth/ # Authentication helpers  
│ ├── datatypes/ # Shared data classes  
│ ├── mongodb_connection/ # MongoDB connection utils  
│ └── langchain_agent/ # Langchain agent memory tools   
</code> </pre>

Each module includes:
- `__init__.py` – Initializes the component
- `core.py` – Primary logic entrypoint
- Other `.py` files – Optional helpers, factories, or submodules

## Testing Components

Each component should be independently testable with unit tests. Test files typically reside in a parallel `tests/` directory at the root level or within each component if co-located.

## Guidelines

- **Reusability First**: Components should be agnostic to deployment targets.
- **Composable**: Design interfaces that make it easy to use from multiple bases.
- **No Side Effects**: Avoid I/O, web servers, or configuration loading inside components.
- **Minimal Dependencies**: Keep dependencies lightweight and relevant to the component’s function.

## Learn More

- [Polylith Architecture Documentation](https://polylith.gitbook.io)
- [Polylith Examples in Python (Unofficial)](https://github.com/polylith/polylith)
