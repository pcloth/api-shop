from __future__ import annotations

from typing import Any, Awaitable, Callable

from ..contracts import ApiError, RequestContext
from ..dispatcher import Dispatcher
from .common import decode_body, encode_body, parse_query


class ASGIAdapter:
    """A dependency-free ASGI catch-all application."""

    def __init__(self, dispatcher: Dispatcher, *, prefix: str = "") -> None:
        self.dispatcher = dispatcher
        self.prefix = "/" + prefix.strip("/") if prefix.strip("/") else ""

    async def __call__(
        self,
        scope: dict[str, Any],
        receive: Callable[[], Awaitable[dict[str, Any]]],
        send: Callable[[dict[str, Any]], Awaitable[None]],
    ) -> None:
        if scope.get("type") != "http":
            raise RuntimeError("ASGIAdapter only supports HTTP scopes")
        path = scope.get("path", "/")
        if self.prefix and path != self.prefix and not path.startswith(self.prefix + "/"):
            response = ApiError(404, "route_not_found", "Route not found").response("")
        else:
            relative_path = path[len(self.prefix) :] or "/"
            raw_body = bytearray()
            while True:
                event = await receive()
                if event.get("type") == "http.disconnect":
                    return
                raw_body.extend(event.get("body", b""))
                if not event.get("more_body", False):
                    break
            headers = {
                key.decode("latin-1"): value.decode("latin-1")
                for key, value in scope.get("headers", ())
            }
            try:
                body, form = decode_body(bytes(raw_body), headers.get("content-type", ""))
            except (UnicodeDecodeError, ValueError):
                context = RequestContext(scope.get("method", "GET"), relative_path, headers=headers)
                response = ApiError(400, "invalid_body", "Request body is invalid").response(
                    context.request_id
                )
            else:
                context = RequestContext(
                    method=scope.get("method", "GET"),
                    path=relative_path,
                    headers=headers,
                    query=parse_query(scope.get("query_string", b"")),
                    body=body,
                    form=form,
                    raw=scope,
                )
                response = await self.dispatcher.dispatch_async(context)
        response_body = encode_body(response.body, response.media_type)
        headers = {**response.headers, "Content-Type": response.media_type}
        await send(
            {
                "type": "http.response.start",
                "status": response.status,
                "headers": [
                    (key.lower().encode("latin-1"), value.encode("latin-1"))
                    for key, value in headers.items()
                ],
            }
        )
        await send({"type": "http.response.body", "body": response_body})

