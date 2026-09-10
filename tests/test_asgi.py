from __future__ import annotations

import asyncio
import json
import unittest
from typing import Annotated

from pydantic import BaseModel

from api_shop import ApiRegistry, Dispatcher, Query
from api_shop.adapters import ASGIAdapter


class SearchInput(BaseModel):
    tag: Annotated[list[str], Query()]


class ASGIAdapterTests(unittest.TestCase):
    def test_repeated_query_values_are_preserved(self):
        registry = ApiRegistry()

        @registry.route("/search", methods=["GET"], input=SearchInput)
        def search(ctx, data):
            return {"tags": data.tag}

        app = ASGIAdapter(Dispatcher(registry), prefix="/api")
        events = [{"type": "http.request", "body": b"", "more_body": False}]
        sent = []

        async def receive():
            return events.pop(0)

        async def send(event):
            sent.append(event)

        scope = {
            "type": "http",
            "method": "GET",
            "path": "/api/search",
            "query_string": b"tag=python&tag=rust",
            "headers": [],
        }
        asyncio.run(app(scope, receive, send))
        self.assertEqual(sent[0]["status"], 200)
        self.assertEqual(json.loads(sent[1]["body"]), {"tags": ["python", "rust"]})


if __name__ == "__main__":
    unittest.main()
