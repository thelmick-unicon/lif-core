"""
This script generates a GraphQL schema from the LIF data model OpenAPI specification
and writes it to a file named `schema.graphql`.  It also generates the schema as JSON
(using introspection) and writes it to a file named `schema.json`.
"""

import json
from graphql import get_introspection_query
from strawberry import Schema
from strawberry.schema.config import StrawberryConfig

from lif.mdr_client import get_openapi_lif_data_model_from_file
from lif.openapi_to_graphql import generate_graphql_root_types
from lif.openapi_to_graphql.schema_tools import get_json_schema_from_introspection

ROOT_TYPE_NAME = "Person"
QUERY_PLANNER_QUERY_URL = "http://localhost:8002/query"
QUERY_PLANNER_UPDATE_URL = "http://localhost:8002/update"

# get the OpenAPI specification for the LIF data model from the MDR
openapi = get_openapi_lif_data_model_from_file()

# keep track of created types, for use later
created_types = {}

# generate the GraphQL root query type from the OpenAPI specification
root_query_type, root_mutation_type = generate_graphql_root_types(
    openapi=openapi,
    root_type_name=ROOT_TYPE_NAME,
    query_planner_query_url=QUERY_PLANNER_QUERY_URL,
    query_planner_update_url=QUERY_PLANNER_UPDATE_URL,
    created_types=created_types,
)

schema_graph = Schema(query=root_query_type, mutation=root_mutation_type, config=StrawberryConfig(auto_camel_case=True))

with open("schema.graphql", "w", encoding="utf-8") as f:
    f.write(schema_graph.as_str())

introspection = schema_graph.execute_sync(get_introspection_query())
if not introspection.errors:
    schema_json = get_json_schema_from_introspection(introspection.data, created_types)
    with open("schema.json", "w", encoding="utf-8") as f:
        json.dump(schema_json, f, indent=2)
else:
    raise ValueError(f"GraphQL introspection failed: {introspection.errors}")
