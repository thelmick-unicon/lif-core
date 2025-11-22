"""
ASGI application generator for OpenAPI-to-GraphQL.

Converts OpenAPI schema definitions to a Strawberry GraphQL API dynamically.
Generates Python types, input filters, enums, and root query objects from OpenAPI JSON schemas.
"""

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from lif.logging import get_logger
from lif.mdr_client import get_openapi_lif_data_model
from lif.openapi_to_graphql.core import generate_graphql_schema

logger = get_logger(__name__)


LIF_QUERY_PLANNER_URL = os.getenv("LIF_QUERY_PLANNER_URL", "http://localhost:8002")
LIF_GRAPHQL_ROOT_TYPE_NAME = os.getenv("LIF_GRAPHQL_ROOT_TYPE_NAME", "Person")

logger.info(f"LIF_QUERY_PLANNER_URL: {LIF_QUERY_PLANNER_URL}")
logger.info(f"LIF_GRAPHQL_ROOT_TYPE_NAME: {LIF_GRAPHQL_ROOT_TYPE_NAME}")
logger.info(f"LIF_MDR_API_URL: {os.getenv('LIF_MDR_API_URL')}")


async def fetch_dynamic_graphql_schema(openapi: dict):
    return await generate_graphql_schema(
        openapi=openapi,
        root_type_name=LIF_GRAPHQL_ROOT_TYPE_NAME,
        query_planner_query_url=LIF_QUERY_PLANNER_URL.rstrip("/") + "/query",
        query_planner_update_url=LIF_QUERY_PLANNER_URL.rstrip("/") + "/update",
    )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    openapi = await get_openapi_lif_data_model()
    schema = await fetch_dynamic_graphql_schema(openapi=openapi)
    logger.info("GraphQL schema successfully created")
    app.include_router(GraphQLRouter(schema, prefix="/graphql"))
    logger.info("GraphQL router successfully created and included in FastAPI app")
    yield


app = FastAPI(lifespan=lifespan)
