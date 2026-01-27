import re
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import jsonref

from lif.logging import get_logger


logger = get_logger(__name__)


@dataclass
class SchemaLeaf:
    """Represents a single leaf node in the OpenAPI schema."""

    json_path: str
    description: str
    attributes: Dict[str, Any]


# TODO: This implementation is different than the one in string_utils.py. Integrate them.
def to_camel_case(s: str) -> str:
    """Convert a string to camelCase."""
    s = re.sub(r"([_\-\s]+)([a-zA-Z])", lambda m: m.group(2).upper(), s)
    if not s:
        return s
    return s[0].lower() + s[1:]


def extract_leaves(obj: Any, path_prefix: str = "", attribute_keys: Optional[List[str]] = None) -> List[SchemaLeaf]:
    """Recursively collect all schema leaves with descriptions."""
    if attribute_keys is None:
        attribute_keys = ["x-queryable", "dataType", "enum", "x-mutable"]
    leaves = []
    if isinstance(obj, dict):
        # Support both "Description" (old schema) and "description" (new schema v2.0)
        # Only use lowercase "description" if it's a string (in old schema, "description"
        # can be a property name containing an object, not the description string)
        desc = obj.get("Description")
        if not desc:
            lowercase_desc = obj.get("description")
            if isinstance(lowercase_desc, str):
                desc = lowercase_desc
        if desc:
            # Preserve original schema property names (e.g., Identifier instead of identifier)
            key = path_prefix.rstrip(".")
            attributes = {to_camel_case(k): obj.get(k) for k in attribute_keys if k in obj}
            leaves.append(SchemaLeaf(json_path=key, description=desc, attributes=attributes))
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                new_prefix = path_prefix
                if k != "properties":
                    new_prefix = f"{path_prefix}.{k}" if path_prefix else k
                leaves.extend(extract_leaves(v, new_prefix, attribute_keys))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            new_prefix = f"{path_prefix}[{i}]"
            leaves.extend(extract_leaves(item, new_prefix, attribute_keys))
    return leaves


def resolve_openapi_root(doc: dict, root: str):
    """Find and return the schema dict for the given root."""
    candidates = []
    if "components" in doc and "schemas" in doc["components"]:
        schemas = doc["components"]["schemas"]
        if root in schemas:
            return schemas[root], root
        candidates.extend(schemas.keys())
    if "definitions" in doc:
        definitions = doc["definitions"]
        if root in definitions:
            return definitions[root], root
        candidates.extend(definitions.keys())
    logger.error(f"Root schema '{root}' not found. Available: {sorted(candidates)}")
    raise ValueError(f"Root schema '{root}' not found.")


def load_schema_leaves(
    openapi_doc: dict, root: Optional[str] = None, attribute_keys: Optional[List[str]] = None
) -> List[SchemaLeaf]:
    """Load and parse OpenAPI dict, returning a flat list of SchemaLeaf objects.

    Args:
        openapi_doc: The OpenAPI document as a Python dictionary.
        root: Root pointer in the OpenAPI doc.
        attribute_keys: Attribute keys to extract from schema.

    Returns:
        List of SchemaLeaf objects representing leaf fields.
    """
    try:
        doc = jsonref.replace_refs(openapi_doc)
    except Exception as e:
        logger.critical(f"Could not resolve refs in OpenAPI doc: {e}")
        sys.exit(1)
    node = doc
    path_prefix = ""
    if root:
        node, path_prefix = resolve_openapi_root(doc, root)
    leaves = extract_leaves(node, path_prefix, attribute_keys)
    return leaves
