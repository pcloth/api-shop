"""Route declaration and deterministic route compilation."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Callable, Iterable, Mapping
from uuid import UUID

from .contracts import ApiError


Handler = Callable[..., Any]


@dataclass(frozen=True, slots=True)
class RouteDefinition:
    path: str
    methods: tuple[str, ...]
    handler: Handler
    input_model: type[Any] | None = None
    responses: Mapping[int, Any] = field(default_factory=dict)
    tags: tuple[str, ...] = ()
    name: str | None = None


@dataclass(frozen=True, slots=True)
class CompiledRoute:
    definition: RouteDefinition
    regex: re.Pattern[str]
    converters: Mapping[str, Callable[[str], Any]]
    signature: str
    priority: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class RouteMatch:
    route: CompiledRoute
    values: Mapping[str, Any]


_CONVERTERS: dict[str, tuple[str, Callable[[str], Any], int]] = {
    "str": (r"[^/]+", str, 2),
    "default": (r"[^/]+", str, 2),
    "int": (r"[0-9]+", int, 3),
    "uuid": (
        r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}",
        UUID,
        3,
    ),
    "slug": (r"[-a-zA-Z0-9_]+", str, 3),
    "path": (r".+", str, 1),
}
_VARIABLE = re.compile(
    r"^<(?:(?P<converter>[A-Za-z_][A-Za-z0-9_]*):)?(?P<name>[A-Za-z_][A-Za-z0-9_]*)>$"
)


class ApiRegistry:
    """Mutable while routes are declared, immutable after :meth:`compile`."""

    def __init__(self) -> None:
        self._definitions: list[RouteDefinition] = []
        self._compiled: tuple[CompiledRoute, ...] | None = None

    @property
    def routes(self) -> tuple[CompiledRoute, ...]:
        if self._compiled is None:
            raise RuntimeError("ApiRegistry must be compiled before it can dispatch")
        return self._compiled

    def route(
        self,
        path: str,
        *,
        methods: Iterable[str],
        input: type[Any] | None = None,
        response: Mapping[int, Any] | Any | None = None,
        tags: Iterable[str] = (),
        name: str | None = None,
    ) -> Callable[[Handler], Handler]:
        if self._compiled is not None:
            raise RuntimeError("Cannot add routes after registry compilation")
        normalized_path = "/" + path.strip("/") if path != "/" else "/"
        normalized_methods = tuple(dict.fromkeys(method.upper() for method in methods))
        if not normalized_methods:
            raise ValueError("A route must declare at least one method")
        if response is None:
            responses: Mapping[int, Any] = {}
        elif isinstance(response, Mapping):
            responses = dict(response)
        else:
            responses = {200: response}

        def decorate(handler: Handler) -> Handler:
            self._definitions.append(
                RouteDefinition(
                    path=normalized_path,
                    methods=normalized_methods,
                    handler=handler,
                    input_model=input,
                    responses=MappingProxyType(dict(responses)),
                    tags=tuple(tags),
                    name=name,
                )
            )
            return handler

        return decorate

    def compile(self) -> "ApiRegistry":
        if self._compiled is not None:
            return self
        compiled: list[CompiledRoute] = []
        seen: dict[tuple[str, str], RouteDefinition] = {}
        for definition in self._definitions:
            route = _compile_route(definition)
            for method in definition.methods:
                conflict = seen.get((method, route.signature))
                if conflict is not None:
                    raise ValueError(
                        f"Ambiguous route for {method}: {conflict.path!r} and {definition.path!r}"
                    )
                seen[(method, route.signature)] = definition
            compiled.append(route)
        compiled.sort(key=lambda item: item.priority, reverse=True)
        self._compiled = tuple(compiled)
        return self

    def match(self, method: str, path: str) -> RouteMatch:
        normalized = "/" + path.strip("/") if path != "/" else "/"
        path_matched = False
        for route in self.routes:
            match = route.regex.fullmatch(normalized)
            if match is None:
                continue
            path_matched = True
            if method.upper() not in route.definition.methods:
                continue
            try:
                values = {
                    name: route.converters[name](value)
                    for name, value in match.groupdict().items()
                }
            except (TypeError, ValueError) as exc:
                raise ApiError(404, "route_not_found", "Route not found") from exc
            return RouteMatch(route, MappingProxyType(values))
        if path_matched:
            allowed = sorted(
                {
                    method_name
                    for route in self.routes
                    if route.regex.fullmatch(normalized)
                    for method_name in route.definition.methods
                }
            )
            raise ApiError(
                405,
                "method_not_allowed",
                "Method not allowed",
                headers={"Allow": ", ".join(allowed)},
            )
        raise ApiError(404, "route_not_found", "Route not found")


def _compile_route(definition: RouteDefinition) -> CompiledRoute:
    if definition.path == "/":
        return CompiledRoute(definition, re.compile(r"/"), MappingProxyType({}), "/", (4,))
    regex_parts: list[str] = []
    signature_parts: list[str] = []
    priorities: list[int] = []
    converters: dict[str, Callable[[str], Any]] = {}
    names: set[str] = set()
    segments = definition.path.strip("/").split("/")
    for index, segment in enumerate(segments):
        variable = _VARIABLE.match(segment)
        if variable is None:
            if "<" in segment or ">" in segment:
                raise ValueError(f"Malformed route segment {segment!r} in {definition.path!r}")
            regex_parts.append(re.escape(segment))
            signature_parts.append(segment)
            priorities.append(4)
            continue
        converter_name = variable.group("converter") or "default"
        name = variable.group("name")
        if name in names:
            raise ValueError(f"Duplicate route variable {name!r} in {definition.path!r}")
        if converter_name not in _CONVERTERS:
            raise ValueError(f"Unknown route converter {converter_name!r}")
        expression, converter, priority = _CONVERTERS[converter_name]
        if converter_name == "path" and index != len(segments) - 1:
            raise ValueError("The path converter must be the final route segment")
        names.add(name)
        converters[name] = converter
        regex_parts.append(f"(?P<{name}>{expression})")
        signature_parts.append(f"<{converter_name}>")
        priorities.append(priority)
    return CompiledRoute(
        definition=definition,
        regex=re.compile("/" + "/".join(regex_parts)),
        converters=MappingProxyType(converters),
        signature="/" + "/".join(signature_parts),
        priority=tuple(priorities),
    )

