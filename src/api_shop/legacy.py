"""Compatibility exports and migration helpers for api-shop 1.x.

The legacy implementation remains available for one major release. New code
should use ApiRegistry and Dispatcher.
"""

from __future__ import annotations

import copy
import importlib
import warnings
from typing import Annotated, Any, Literal

from pydantic import Field, create_model

from .api_shop import (
    Api,
    ApiDataClass,
    ApiResponseModelFields,
    ApiShop,
    SingleApiShop,
    get_api_result_json,
    get_api_result_response,
    get_single_apishop,
    return_response,
    single_apishop,
)
from .contracts import LegacyAuto, Path
from .dispatcher import Dispatcher
from .registry import ApiRegistry


def dispatcher_from_conf(conf: list[dict[str, Any]], *, middleware=()) -> Dispatcher:
    """Translate a 1.x configuration into the v2 dispatcher.

    Legacy fields without a path variable use path > JSON body > form > query
    precedence. The input configuration is copied and never modified.
    """
    warnings.warn(
        "Legacy conf translation is deprecated; migrate endpoints to typed contracts",
        DeprecationWarning,
        stacklevel=2,
    )
    registry = ApiRegistry()
    for api_index, api_conf in enumerate(copy.deepcopy(conf)):
        handler_class = _load_handler(api_conf["class"])
        urls = api_conf["url"] if isinstance(api_conf["url"], list) else [api_conf["url"]]
        for method, parameters in api_conf.get("methods", {}).items():
            method_name = method.lower()
            if not hasattr(handler_class, method_name):
                raise TypeError(f"Legacy handler {handler_class.__name__} has no {method_name} method")
            for url_index, url in enumerate(urls):
                input_model = _legacy_input_model(
                    f"LegacyInput{api_index}_{method}_{url_index}", url, parameters
                )

                def invoke(ctx, data, cls=handler_class, method_key=method_name):
                    instance = object.__new__(cls)
                    return getattr(instance, method_key)(ctx.raw or ctx, data)

                registry.route(
                    url,
                    methods=[method],
                    input=input_model,
                    tags=[api_conf.get("name", "legacy")],
                    name=f"legacy_{api_index}_{method_name}_{url_index}",
                )(invoke)
    return Dispatcher(registry, middleware=middleware)


def _load_handler(value: Any) -> type[Any]:
    if not isinstance(value, str):
        return value
    module_name, separator, attribute = value.rpartition(".")
    if not separator:
        raise ImportError(f"Legacy handler path must include a module: {value!r}")
    module = importlib.import_module(module_name)
    return getattr(module, attribute)


def _legacy_input_model(name: str, url: str, parameters: list[dict[str, Any]]) -> type[Any]:
    path_names = {
        segment.rsplit(":", 1)[-1].rstrip(">")
        for segment in url.split("/")
        if segment.startswith("<") and segment.endswith(">")
    }
    fields: dict[str, tuple[Any, Any]] = {}
    for parameter in parameters:
        field_name = parameter["name"]
        annotation = parameter.get("type") or Any
        options = parameter.get("options")
        if options:
            annotation = Literal.__getitem__(tuple(options))
        source = Path() if field_name in path_names else LegacyAuto()
        annotated = Annotated[annotation, source]
        field_args: dict[str, Any] = {"description": parameter.get("description")}
        minimum = parameter.get("min")
        maximum = parameter.get("max")
        if annotation in (str, list, set, tuple, dict):
            if minimum is not None:
                field_args["min_length"] = minimum
            if maximum is not None:
                field_args["max_length"] = maximum
        elif annotation in (int, float):
            if minimum is not None:
                field_args["ge"] = minimum
            if maximum is not None:
                field_args["le"] = maximum
        if "default" in parameter:
            default = parameter["default"]
        elif parameter.get("required"):
            default = ...
        else:
            default = None
        fields[field_name] = (annotated, Field(default, **field_args))
    return create_model(name, **fields)

__all__ = [
    "Api",
    "ApiDataClass",
    "ApiResponseModelFields",
    "ApiShop",
    "SingleApiShop",
    "get_api_result_json",
    "get_api_result_response",
    "get_single_apishop",
    "return_response",
    "single_apishop",
    "dispatcher_from_conf",
]
