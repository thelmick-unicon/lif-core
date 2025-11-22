
# `test/` Directory

This directory contains unit tests and integration tests for the `components/` and `bases/` of the LIF system, following the Polylith architectural pattern. All tests are written in pure Python, using standard testing libraries like `unittest` or `pytest`.

## Purpose

The `test/` directory is designed to:
- Ensure correctness of reusable components (`components/`)
- Validate the orchestration logic in deployable services (`bases/`)
- Enable fast feedback during development and CI/CD
- Promote a clean separation between logic and test code

## Example Structure

The directory layout mirrors the source tree of `components/` and `bases/`:

<pre lang="markdown"> <code> 
test/  
├── components/  
│ └── lif/  
│ ├── query_cache_service/  
│ │ └── test_core.py  
│ └── openapi_to_graphql/  
│ └── test_core.py  
│ ...  
├── bases/  
│ └── lif/  
│ ├── api_graphql/  
│ │ └── test_core.py  
│ └── advisor_restapi/  
│ └── test_core.py
</code> </pre>

Each module typically contains:
- `test_core.py` — tests for the corresponding `core.py`
- `__init__.py` — marks the directory as a Python module (optional with modern Python)

## Setup

For now, export `LIF_ADAPTER__LIF_TO_LIF__GRAPHQL_API_URL` with an arbitrary value before running the tests, such as:

```bash
export LIF_ADAPTER__LIF_TO_LIF__GRAPHQL_API_URL="asdf"
```

## Running Tests

You can run all tests using `pytest` or another test runner of your choice:

    pytest test/

To run a specific module:

    pytest test/components/lif/query_cache_service/test_core.py

## Guidelines

-   Mirror the structure of the source directories (`components/` and `bases/`)
-   Keep test cases focused and descriptive
-   Use test doubles (e.g., mocks or fixtures) to isolate logic
-   Group related tests into classes or logical sections
-   Prefer small, fast, and deterministic tests

## Related Directories

-   `components/`: Reusable feature modules tested here
-   `bases/`: Deployment contexts tested here
-   `development/`: May contain mock data or helper scripts used during testing

## Recommended Tools

-   pytest
-   [unittest](https://docs.python.org/3/library/unittest.html)
-   [coverage.py](https://coverage.readthedocs.io/) — for test coverage reporting
