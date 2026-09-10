from __future__ import annotations

from typing import Any

from ..contracts import RequestContext
from ..dispatcher import Dispatcher
from .common import collapse_pairs, encode_body


def mount_flask(app: Any, dispatcher: Dispatcher, *, prefix: str = "/api", endpoint: str = "api_shop") -> None:
    """Mount one Flask catch-all. Flask is imported only when this function is used."""
    from flask import request

    normalized = "/" + prefix.strip("/")

    def view(path: str = "") -> Any:
        body = request.get_json(silent=True)
        context = RequestContext(
            method=request.method,
            path="/" + path,
            headers=dict(request.headers),
            query=collapse_pairs(request.args.items(multi=True)),
            cookies=dict(request.cookies),
            body=body,
            form=collapse_pairs(request.form.items(multi=True)),
            files=dict(request.files),
            raw=request,
        )
        result = dispatcher.dispatch(context)
        return app.response_class(
            encode_body(result.body, result.media_type),
            status=result.status,
            headers=result.headers,
            content_type=result.media_type,
        )

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]
    app.add_url_rule(normalized, endpoint, view, defaults={"path": ""}, methods=methods)
    app.add_url_rule(normalized + "/<path:path>", endpoint + "_path", view, methods=methods)

