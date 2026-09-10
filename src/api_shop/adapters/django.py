from __future__ import annotations

import re
from typing import Any

from ..contracts import RequestContext
from ..dispatcher import Dispatcher
from .common import collapse_lists, decode_body, encode_body


def django_urlpatterns(dispatcher: Dispatcher, *, prefix: str = "api") -> list[Any]:
    """Return a single Django catch-all URL pattern."""
    from django.http import HttpResponse
    from django.urls import re_path

    def view(request: Any, path: str = "") -> Any:
        content_type = request.headers.get("Content-Type", "")
        try:
            body, form_body = decode_body(request.body, content_type)
        except (UnicodeDecodeError, ValueError):
            body, form_body = None, {}
        form = collapse_lists(request.POST.lists()) if request.POST else form_body
        query = collapse_lists(request.GET.lists())
        context = RequestContext(
            method=request.method,
            path="/" + path,
            headers=dict(request.headers),
            query=query,
            cookies=request.COOKIES,
            body=body,
            form=form,
            files=request.FILES,
            raw=request,
        )
        result = dispatcher.dispatch(context)
        return HttpResponse(
            encode_body(result.body, result.media_type),
            status=result.status,
            headers=result.headers,
            content_type=result.media_type,
        )

    normalized = prefix.strip("/")
    expression = rf"^{re.escape(normalized)}/?(?P<path>.*)$" if normalized else r"^(?P<path>.*)$"
    return [re_path(expression, view, name="api-shop")]
