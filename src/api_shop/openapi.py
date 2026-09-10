"""OpenAPI 3.1 generation from compiled runtime contracts."""

from __future__ import annotations

import re
from typing import Any

from pydantic import TypeAdapter

from .contracts import Body, Cookie, File, Form, Header, LegacyAuto, Path, Query
from .registry import ApiRegistry


def generate_openapi(
    registry: ApiRegistry,
    *,
    title: str,
    version: str,
    description: str | None = None,
) -> dict[str, Any]:
    document: dict[str, Any] = {
        "openapi": "3.1.0",
        "info": {"title": title, "version": version},
        "paths": {},
    }
    if description:
        document["info"]["description"] = description
    for route in registry.routes:
        path = re.sub(r"<(?:[A-Za-z_][A-Za-z0-9_]*:)?([A-Za-z_][A-Za-z0-9_]*)>", r"{\1}", route.definition.path)
        path_item = document["paths"].setdefault(path, {})
        for method in route.definition.methods:
            operation: dict[str, Any] = {
                "operationId": route.definition.name or route.definition.handler.__name__,
                "tags": list(route.definition.tags),
                "parameters": [],
                "responses": {},
            }
            model = route.definition.input_model
            body_properties: dict[str, Any] = {}
            body_required: list[str] = []
            body_content_type = "application/json"
            whole_body_schema: dict[str, Any] | None = None
            whole_body_required = False
            if model is not None:
                for name, field in model.model_fields.items():
                    source = next(
                        item
                        for item in field.metadata
                        if isinstance(item, (Path, Query, Header, Cookie, Body, Form, File, LegacyAuto))
                    )
                    alias = source.alias or field.alias or name
                    schema = TypeAdapter(field.annotation).json_schema()
                    required = field.is_required()
                    if isinstance(source, Body):
                        whole_body_schema = schema
                        whole_body_required = required
                    elif isinstance(source, (Form, File)):
                        body_properties[alias] = schema
                        if required:
                            body_required.append(alias)
                        body_content_type = "multipart/form-data"
                    elif isinstance(source, LegacyAuto):
                        operation["parameters"].append(
                            {
                                "name": alias,
                                "in": "query",
                                "required": required,
                                "schema": schema,
                                "x-api-shop-legacy-auto": True,
                            }
                        )
                    else:
                        location = {
                            Path: "path",
                            Query: "query",
                            Header: "header",
                            Cookie: "cookie",
                        }[type(source)]
                        operation["parameters"].append(
                            {
                                "name": alias,
                                "in": location,
                                "required": True if location == "path" else required,
                                "schema": schema,
                            }
                        )
            if whole_body_schema is not None or body_properties:
                body_schema: dict[str, Any]
                if whole_body_schema is not None:
                    body_schema = whole_body_schema
                else:
                    body_schema = {"type": "object", "properties": body_properties}
                if body_required:
                    body_schema["required"] = body_required
                operation["requestBody"] = {
                    "required": whole_body_required or bool(body_required),
                    "content": {body_content_type: {"schema": body_schema}},
                }
            for status, response_type in route.definition.responses.items():
                operation["responses"][str(status)] = {
                    "description": "Response",
                    "content": {
                        "application/json": {"schema": TypeAdapter(response_type).json_schema()}
                    },
                }
            if not operation["responses"]:
                operation["responses"]["200"] = {"description": "Response"}
            path_item[method.lower()] = operation
    return document
