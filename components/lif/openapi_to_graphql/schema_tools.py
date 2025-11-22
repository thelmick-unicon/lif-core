from enum import Enum
from typing import Any, Dict, Type

from lif.logging import get_logger

logger = get_logger(__name__)


def graphql_type_to_json_schema(
    gql_type: Dict[str, Any], type_map: Dict[str, Any], created_types: Dict[str, Any]
) -> Dict[str, Any]:
    """Convert a GraphQL type (from introspection) to a JSON Schema fragment."""
    if gql_type["kind"] == "NON_NULL":
        return graphql_type_to_json_schema(gql_type["ofType"], type_map, created_types)
    if gql_type["kind"] == "LIST":
        return {"type": "array", "items": graphql_type_to_json_schema(gql_type["ofType"], type_map, created_types)}
    if gql_type["kind"] == "SCALAR":
        if gql_type["name"] in ["String", "ID"]:
            return {"type": "string"}
        elif gql_type["name"] == "Int":
            return {"type": "integer"}
        elif gql_type["name"] == "Float":
            return {"type": "number"}
        elif gql_type["name"] == "Boolean":
            return {"type": "boolean"}
        else:
            return {"type": "string"}
    if gql_type["kind"] == "ENUM":
        enum_type = type_map[gql_type["name"]]
        enum_cls = created_types.get(gql_type["name"])
        if enum_cls:
            enum_values = [
                getattr(enum_cls, ev["name"]).value
                for ev in enum_type.get("enumValues", [])
                if not ev.get("isDeprecated", False)
            ]
        else:
            enum_values = [ev["name"] for ev in enum_type.get("enumValues", []) if not ev.get("isDeprecated", False)]
        return {"type": "string", "enum": enum_values}
    return {"$ref": f"#/definitions/{gql_type['name']}"}


def get_json_schema_from_introspection(
    introspection: Dict[str, Any], created_types: Dict[str, Type[Enum]]
) -> Dict[str, Any]:
    """Convert GraphQL introspection result (as dict) to a JSON Schema draft-07 object.

    Args:
        introspection (Dict[str, Any]): The result.data dict from a GraphQL introspection query.

    Returns:
        Dict[str, Any]: JSON Schema root object.
    """
    types = introspection["__schema"]["types"]
    type_map = {t["name"]: t for t in types}

    json_schema: Dict[str, Any] = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Query",
        "type": "object",
        "properties": {},
        "definitions": {},
        "additionalProperties": False,
    }

    for t in types:
        if t["kind"] == "OBJECT" and not t["name"].startswith("__"):
            props = {}
            required = []
            for f in t.get("fields", []):
                props[f["name"]] = graphql_type_to_json_schema(f["type"], type_map, created_types)
                if f["type"]["kind"] == "NON_NULL":
                    required.append(f["name"])
            json_schema["definitions"][t["name"]] = {
                "type": "object",
                "properties": props,
                "required": required,
                "additionalProperties": False,
            }
        elif t["kind"] == "ENUM":
            # Define enum as its own definition
            enum_cls = created_types.get(t["name"])

            if enum_cls:
                enum_values = [
                    getattr(enum_cls, ev["name"]).value
                    for ev in t.get("enumValues", [])
                    if not ev.get("isDeprecated", False)
                ]
            else:
                enum_values = [ev["name"] for ev in t.get("enumValues", []) if not ev.get("isDeprecated", False)]

            json_schema["definitions"][t["name"]] = {
                "type": "string",
                "enum": enum_values,
                "description": t.get("description", "") or "",
            }

    # Top-level (Query) properties
    query_type = next(t for t in types if t["name"] == "Query")
    for f in query_type["fields"]:
        json_schema["properties"][f["name"]] = graphql_type_to_json_schema(f["type"], type_map, created_types)
    return json_schema
