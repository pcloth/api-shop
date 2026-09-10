from __future__ import annotations

from typing import Any

from ..contracts import RequestContext
from ..dispatcher import Dispatcher
from .common import collapse_pairs, encode_body


def mount_bottle(app: Any, dispatcher: Dispatcher, *, prefix: str = "/api") -> None:
    """Mount one Bottle catch-all route."""
    from bottle import HTTPResponse, request

    normalized = "/" + prefix.strip("/")

    def view(path: str = "") -> Any:
        context = RequestContext(
            method=request.method,
            path="/" + path,
            headers=dict(request.headers),
            query=collapse_pairs(request.query.allitems()),
            cookies=dict(request.cookies),
            body=request.json,
            form=collapse_pairs(request.forms.allitems()),
            files=dict(request.files),
            raw=request,
        )
        result = dispatcher.dispatch(context)
        return HTTPResponse(
            body=encode_body(result.body, result.media_type),
            status=result.status,
            headers={**result.headers, "Content-Type": result.media_type},
        )

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]
    app.route(normalized, methods, view)
    app.route(normalized + "/<path:path>", methods, view)

