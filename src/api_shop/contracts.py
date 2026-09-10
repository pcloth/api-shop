"""Framework-neutral request, response, binding, and error contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, MutableMapping
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class Source:
    alias: str | None = None


@dataclass(frozen=True, slots=True)
class Path(Source):
    pass


@dataclass(frozen=True, slots=True)
class Query(Source):
    pass


@dataclass(frozen=True, slots=True)
class Header(Source):
    pass


@dataclass(frozen=True, slots=True)
class Cookie(Source):
    pass


@dataclass(frozen=True, slots=True)
class Body(Source):
    """Bind the complete decoded request body to a model field."""


@dataclass(frozen=True, slots=True)
class Form(Source):
    pass


@dataclass(frozen=True, slots=True)
class File(Source):
    pass


@dataclass(frozen=True, slots=True)
class LegacyAuto(Source):
    """Compatibility-only source using the documented 1.x precedence."""


@dataclass(slots=True)
class RequestContext:
    method: str
    path: str
    headers: Mapping[str, Any] = field(default_factory=dict)
    query: Mapping[str, Any] = field(default_factory=dict)
    cookies: Mapping[str, Any] = field(default_factory=dict)
    body: Any = None
    form: Mapping[str, Any] = field(default_factory=dict)
    files: Mapping[str, Any] = field(default_factory=dict)
    state: MutableMapping[str, Any] = field(default_factory=dict)
    raw: Any = None
    path_params: Mapping[str, Any] = field(default_factory=dict)
    request_id: str = ""

    def __post_init__(self) -> None:
        self.method = self.method.upper()
        if not self.path.startswith("/"):
            self.path = "/" + self.path
        if not self.request_id:
            headers = {str(k).lower(): v for k, v in self.headers.items()}
            self.request_id = str(headers.get("x-request-id") or uuid4())


@dataclass(slots=True)
class ResponseContext:
    body: Any = None
    status: int = 200
    headers: MutableMapping[str, str] = field(default_factory=dict)
    media_type: str = "application/json"


class ApiError(Exception):
    def __init__(
        self,
        status: int,
        code: str,
        message: str,
        *,
        details: list[dict[str, Any]] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message
        self.details = details or []
        self.headers = dict(headers or {})

    def response(self, request_id: str) -> ResponseContext:
        return ResponseContext(
            status=self.status,
            headers=self.headers,
            body={
                "error": {
                    "code": self.code,
                    "message": self.message,
                    "details": self.details,
                    "request_id": request_id,
                }
            },
        )


BindingSource = Path | Query | Header | Cookie | Body | Form | File | LegacyAuto
