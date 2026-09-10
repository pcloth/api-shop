from __future__ import annotations

import io
import json
import unittest
from typing import Annotated

from pydantic import BaseModel

from api_shop import ApiRegistry, Dispatcher, Query
from api_shop.adapters import django_urlpatterns, mount_bottle, mount_flask


class TagsInput(BaseModel):
    tag: Annotated[list[str], Query()]


def make_dispatcher():
    registry = ApiRegistry()

    @registry.route("/search", methods=["GET"], input=TagsInput)
    def search(ctx, data):
        return {"tags": data.tag}

    return Dispatcher(registry)


class FlaskAdapterTests(unittest.TestCase):
    def test_catch_all_and_repeated_query(self):
        from flask import Flask

        app = Flask(__name__)
        mount_flask(app, make_dispatcher(), prefix="/api")
        response = app.test_client().get("/api/search?tag=python&tag=rust")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"tags": ["python", "rust"]})


class DjangoAdapterTests(unittest.TestCase):
    def test_catch_all_and_repeated_query(self):
        from django.conf import settings

        if not settings.configured:
            settings.configure(DEFAULT_CHARSET="utf-8")
        from django.test import RequestFactory

        pattern = django_urlpatterns(make_dispatcher(), prefix="api")[0]
        request = RequestFactory().get("/api/search?tag=python&tag=rust")
        response = pattern.callback(request, path="search")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"tags": ["python", "rust"]})


class BottleAdapterTests(unittest.TestCase):
    def test_catch_all_and_repeated_query(self):
        from bottle import Bottle

        app = Bottle()
        mount_bottle(app, make_dispatcher(), prefix="/api")
        environ = {
            "REQUEST_METHOD": "GET",
            "PATH_INFO": "/api/search",
            "QUERY_STRING": "tag=python&tag=rust",
            "SERVER_NAME": "localhost",
            "SERVER_PORT": "80",
            "SERVER_PROTOCOL": "HTTP/1.1",
            "wsgi.version": (1, 0),
            "wsgi.url_scheme": "http",
            "wsgi.input": io.BytesIO(b""),
            "wsgi.errors": io.StringIO(),
            "wsgi.multithread": False,
            "wsgi.multiprocess": False,
            "wsgi.run_once": False,
        }
        captured = {}

        def start_response(status, headers, exc_info=None):
            captured["status"] = status
            captured["headers"] = headers

        body = b"".join(app(environ, start_response))
        self.assertTrue(captured["status"].startswith("200"))
        self.assertEqual(json.loads(body), {"tags": ["python", "rust"]})
