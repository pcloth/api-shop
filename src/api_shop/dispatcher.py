"""Validation, middleware execution, handler invocation, and serialization."""

from __future__ import annotations

import asyncio
import inspect
import logging
import types
from collections.abc import Awaitable, Callable, Mapping, Sequence
from typing import Any, get_args, get_origin

from pydantic import BaseModel, TypeAdapter, ValidationError

from .contracts import (
    ApiError,
    BindingSource,
    Body,
    Cookie,
    File,
    Form,
    Header,
    LegacyAuto,
    Path,
    Query,
    RequestContext,
    ResponseContext,
)
from .registry import ApiRegistry, CompiledRoute


Next = Callable[[RequestContext], Awaitable[ResponseContext]]
Middleware = Callable[[RequestContext, Next], ResponseContext | Awaitable[ResponseContext]]


class Dispatcher:
    def __init__(
        self,
        registry: ApiRegistry,
        *,
        middleware: Sequence[Middleware] = (),
        logger: logging.Logger | None = None,
    ) -> None:
        self.registry = registry.compile()
        self.middleware = tuple(middleware)
        self.logger = logger or logging.getLogger("api_shop")
        for route in self.registry.routes:
            _validate_input_contract(route)

    async def dispatch_async(self, request: RequestContext) -> ResponseContext:
        async def endpoint(context: RequestContext) -> ResponseContext:
            return await self._invoke(context)

        next_handler = endpoint
        for middleware in reversed(self.middleware):
            downstream = next_handler

            async def wrapped(
                context: RequestContext,
                current: Middleware = middleware,
                following: Next = downstream,
            ) -> ResponseContext:
                return await _await_if_needed(current(context, following))

            next_handler = wrapped
        try:
            response = await next_handler(request)
        except ApiError as exc:
            response = exc.response(request.request_id)
        except Exception:
            self.logger.exception("Unhandled API exception", extra={"request_id": request.request_id})
            response = ApiError(500, "internal_error", "Internal server error").response(
                request.request_id
            )
        response.headers.setdefault("X-Request-ID", request.request_id)
        return response

    def dispatch(self, request: RequestContext) -> ResponseContext:
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(self.dispatch_async(request))
        raise RuntimeError("dispatch() cannot run inside an event loop; use dispatch_async()")

    async def _invoke(self, request: RequestContext) -> ResponseContext:
        matched = self.registry.match(request.method, request.path)
        request.path_params = matched.values
        data = _bind_input(matched.route, request)
        result = matched.route.definition.handler(request, data)
        result = await _await_if_needed(result)
        response = _normalize_response(result)
        return _validate_response(matched.route, response, request.request_id, self.logger)


async def _await_if_needed(value: Any) -> Any:
    if inspect.isawaitable(value):
        return await value
    return value


def _validate_input_contract(route: CompiledRoute) -> None:
    model = route.definition.input_model
    if model is None:
        return
    if not isinstance(model, type) or not issubclass(model, BaseModel):
        raise TypeError(f"Input contract for {route.definition.path!r} must inherit pydantic.BaseModel")
    path_names = set(route.converters)
    bound_paths: set[str] = set()
    body_fields: list[str] = []
    structured_body_fields: list[str] = []
    for name, field in model.model_fields.items():
        source = _field_source(field.metadata)
        if source is None:
            raise TypeError(f"Input field {model.__name__}.{name} must declare a binding source")
        if isinstance(source, Path):
            bound_paths.add(source.alias or field.alias or name)
        elif isinstance(source, Body):
            body_fields.append(name)
        elif isinstance(source, (Form, File)):
            structured_body_fields.append(name)
    if len(body_fields) > 1:
        raise TypeError("An input contract may declare only one whole-body field")
    if body_fields and structured_body_fields:
        raise TypeError("Body cannot be mixed with Form or File bindings")
    if path_names != bound_paths:
        raise TypeError(
            f"Path bindings for {route.definition.path!r} do not match route variables: "
            f"expected {sorted(path_names)}, got {sorted(bound_paths)}"
        )


def _field_source(metadata: list[Any]) -> BindingSource | None:
    sources = [
        item
        for item in metadata
        if isinstance(item, (Path, Query, Header, Cookie, Body, Form, File, LegacyAuto))
    ]
    if len(sources) > 1:
        raise TypeError("An input field may declare only one binding source")
    return sources[0] if sources else None


def _bind_input(route: CompiledRoute, request: RequestContext) -> Any:
    model = route.definition.input_model
    if model is None:
        return None
    values: dict[str, Any] = {}
    lower_headers = {str(key).lower(): value for key, value in request.headers.items()}
    for name, field in model.model_fields.items():
        source = _field_source(field.metadata)
        assert source is not None
        alias = source.alias or field.alias or name
        missing = object()
        value: Any = missing
        if isinstance(source, Path):
            value = request.path_params.get(alias, missing)
        elif isinstance(source, Query):
            value = request.query.get(alias, missing)
        elif isinstance(source, Header):
            value = lower_headers.get(alias.lower(), missing)
        elif isinstance(source, Cookie):
            value = request.cookies.get(alias, missing)
        elif isinstance(source, Body):
            value = request.body if request.body is not None else missing
        elif isinstance(source, Form):
            value = request.form.get(alias, missing)
        elif isinstance(source, File):
            value = request.files.get(alias, missing)
        elif isinstance(source, LegacyAuto):
            if alias in request.path_params:
                value = request.path_params[alias]
            elif isinstance(request.body, Mapping) and alias in request.body:
                value = request.body[alias]
            elif alias in request.form:
                value = request.form[alias]
            elif alias in request.query:
                value = request.query[alias]
        if value is not missing:
            if _contains_bool(field.annotation):
                try:
                    value = _strict_bool(value)
                except ValueError as exc:
                    raise ApiError(
                        422,
                        "validation_error",
                        "Request validation failed",
                        details=[
                            {
                                "location": [source.__class__.__name__.lower(), name],
                                "code": "bool_parsing",
                                "message": "Value must be true, false, 1, or 0",
                            }
                        ],
                    ) from exc
            values[name] = value
    try:
        return model.model_validate(values)
    except ValidationError as exc:
        details = []
        for error in exc.errors(include_url=False):
            location = list(error.get("loc", ()))
            field_name = str(location[0]) if location else ""
            source = _field_source(model.model_fields[field_name].metadata) if field_name in model.model_fields else None
            source_name = source.__class__.__name__.lower() if source else "request"
            details.append(
                {
                    "location": [source_name, *location],
                    "code": error.get("type", "validation_error"),
                    "message": error.get("msg", "Invalid value"),
                }
            )
        raise ApiError(422, "validation_error", "Request validation failed", details=details) from exc


def _contains_bool(annotation: Any) -> bool:
    if annotation is bool:
        return True
    origin = get_origin(annotation)
    if origin in (types.UnionType, __import__("typing").Union):
        return bool in get_args(annotation)
    return False


def _strict_bool(value: Any) -> bool | None:
    if value is None or isinstance(value, bool):
        return value
    if value in (0, "0"):
        return False
    if value in (1, "1"):
        return True
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized == "true":
            return True
        if normalized == "false":
            return False
    raise ValueError("invalid boolean")


def _normalize_response(result: Any) -> ResponseContext:
    if isinstance(result, ResponseContext):
        return result
    if isinstance(result, tuple):
        if len(result) != 2:
            raise TypeError("Handler tuple responses must be (body, status)")
        return ResponseContext(body=result[0], status=int(result[1]))
    return ResponseContext(body=result)


def _validate_response(
    route: CompiledRoute,
    response: ResponseContext,
    request_id: str,
    logger: logging.Logger,
) -> ResponseContext:
    expected = route.definition.responses.get(response.status)
    if expected is None:
        if route.definition.responses:
            logger.error(
                "Handler returned undeclared status %s",
                response.status,
                extra={"request_id": request_id, "route": route.definition.path},
            )
            raise ApiError(500, "response_validation_error", "Response validation failed")
        return response
    try:
        adapter = TypeAdapter(expected)
        validated = adapter.validate_python(response.body)
        response.body = adapter.dump_python(validated, mode="json")
        return response
    except ValidationError as exc:
        logger.error(
            "Response contract validation failed: %s",
            exc,
            extra={"request_id": request_id, "route": route.definition.path},
        )
        raise ApiError(500, "response_validation_error", "Response validation failed") from exc
