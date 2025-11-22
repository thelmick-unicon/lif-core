import json
import os
import sys
from typing import Annotated, List

from fastmcp import FastMCP
from pydantic import Field
from sentence_transformers import SentenceTransformer
from starlette.requests import Request
from starlette.responses import PlainTextResponse

from lif.logging import get_logger
from lif.mdr_client import get_openapi_lif_data_model_from_file
from lif.openapi_schema_parser import load_schema_leaves
from lif.semantic_search_service.core import (
    build_embeddings,
    run_semantic_search,
    build_dynamic_filter_model,
    build_dynamic_mutation_model,
    run_mutation,
)

logger = get_logger(__name__)


# --------- LOAD ENVIRONMENT VARIABLES ---------

ROOT_NODE = os.getenv("LIF_GRAPHQL_ROOT_NODE", "Person")
LIF_GRAPHQL_API_URL = os.getenv("LIF_GRAPHQL_API_URL", "http://localhost:8002/graphql")
TOP_K = int(os.getenv("TOP_K", 200))
MODEL_NAME = "all-MiniLM-L6-v2"

ATTRIBUTE_KEYS = ["x-queryable", "x-mutable", "DataType", "Required", "Array", "enum"]  # Add more attributes as needed


# --------- LOAD VECTOR STORE & EMBEDDINGS ---------

# get the OpenAPI specification for the LIF data model from the MDR
openapi = get_openapi_lif_data_model_from_file()

try:
    LEAVES = load_schema_leaves(openapi, ROOT_NODE, attribute_keys=ATTRIBUTE_KEYS)
except Exception as e:
    logger.critical(f"Failed to load schema leaves: {e}")
    sys.exit(1)

try:
    FILTER = build_dynamic_filter_model(LEAVES)
    Filter = FILTER[ROOT_NODE]
    logger.info("Dynamic Filter Schema:\n" + json.dumps(Filter.model_json_schema(), indent=2))
except Exception as e:
    logger.critical(f"Failed to load build dynamic filter model: {e}")
    sys.exit(1)

try:
    MUTATION_MODELS = build_dynamic_mutation_model(LEAVES)
    MutationModel = MUTATION_MODELS[ROOT_NODE]
    logger.info("Dynamic Mutation Schema:\n" + json.dumps(MutationModel.model_json_schema(), indent=2))
except Exception as e:
    logger.critical(f"Failed to build dynamic mutation model: {e}")
    sys.exit(1)

try:
    MODEL = SentenceTransformer(MODEL_NAME)
except Exception as e:
    logger.critical(f"Failed to load SentenceTransformer model: {e}")
    sys.exit(1)

# ------ ALWAYS embed only the descriptions ------
EMBEDDING_TEXTS = [leaf.description for leaf in LEAVES]

try:
    EMBEDDINGS = build_embeddings(EMBEDDING_TEXTS, MODEL)
except Exception as e:
    logger.critical(f"EMBEDDINGS failed: {e}")
    sys.exit(1)


mcp = FastMCP(name="LIF-Query-Server")


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("OK")


@mcp.tool(
    name="lif_query", description="Use this tool to run a LIF data query", annotations={"title": "Execute LIF Query"}
)
async def lif_query(
    filter: Annotated[Filter, Field(description="Parameters for LIF query")],
    query: Annotated[str, Field(description="Natural language query used to determine LIF data to retrieve")],
) -> List[dict]:
    return await run_semantic_search(
        filter=filter,
        query=query,
        model=MODEL,
        embeddings=EMBEDDINGS,
        leaves=LEAVES,
        top_k=TOP_K,
        graphql_url=LIF_GRAPHQL_API_URL,
    )


@mcp.tool(
    name="lif_mutation",
    description="Use this tool to mutate/update LIF data fields. You must specify a filter to select records.",
    annotations={"title": "Execute LIF Mutation"},
)
async def lif_mutation(
    filter: Annotated[Filter, Field(description="Filter to select records for mutation")],
    input: Annotated[MutationModel, Field(description="Fields to update")],
) -> dict:
    """Run a mutation on LIF data fields."""
    return await run_mutation(filter=filter, input=input, graphql_url=LIF_GRAPHQL_API_URL)


http_app = mcp.http_app()
