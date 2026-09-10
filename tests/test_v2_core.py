from __future__ import annotations

import asyncio
import unittest
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

from api_shop import (
    ApiRegistry,
    Body,
    Dispatcher,
    Header,
    Path,
    Query,
    RequestContext,
    ResponseContext,
    generate_openapi,
)


class UserBody(BaseModel):
    name: str = Field(min_length=2)


class UserInput(BaseModel):
    user_id: Annotated[int, Path()]
    verbose: Annotated[bool, Query()] = False
    token: Annotated[str, Header(alias="Authorization")]
    body: Annotated[UserBody, Body()]


class UserOutput(BaseModel):
    id: int
    name: str


def make_dispatcher(*, handler=None, middleware=()):
    registry = ApiRegistry()

    @registry.route(
        "/users/<int:user_id>",
        methods=["PATCH"],
        input=UserInput,
        response={200: UserOutput},
        tags=["users"],
        name="update_user",
    )
    async def update_user(ctx, data):
        if handler:
            return await handler(ctx, data)
        return {"id": data.user_id, "name": data.body.name}

    return registry, Dispatcher(registry, middleware=middleware)


class DispatcherTests(unittest.TestCase):
    def request(self, **overrides):
        values = {
            "method": "PATCH",
            "path": "/users/12",
            "query": {"verbose": "false"},
            "headers": {"authorization": "secret"},
            "body": {"name": "Ada"},
        }
        values.update(overrides)
        return RequestContext(**values)

    def test_binding_and_response_validation(self):
        _, dispatcher = make_dispatcher()
        response = dispatcher.dispatch(self.request())
        self.assertEqual(response.status, 200)
        self.assertEqual(response.body, {"id": 12, "name": "Ada"})
        self.assertIn("X-Request-ID", response.headers)

    def test_strict_boolean_rejects_garbage(self):
        _, dispatcher = make_dispatcher()
        response = dispatcher.dispatch(self.request(query={"verbose": "garbage"}))
        self.assertEqual(response.status, 422)
        self.assertEqual(response.body["error"]["code"], "validation_error")
        self.assertEqual(response.body["error"]["details"][0]["location"][0], "query")

    def test_boolean_does_not_accept_pydantic_yes_no_coercion(self):
        _, dispatcher = make_dispatcher()
        response = dispatcher.dispatch(self.request(query={"verbose": "yes"}))
        self.assertEqual(response.status, 422)

    def test_invalid_response_is_hidden_and_returns_500(self):
        async def invalid(ctx, data):
            return {"id": "not-an-int", "name": data.body.name}

        _, dispatcher = make_dispatcher(handler=invalid)
        response = dispatcher.dispatch(self.request())
        self.assertEqual(response.status, 500)
        self.assertEqual(response.body["error"]["code"], "response_validation_error")

    def test_undeclared_response_status_returns_500(self):
        async def undeclared(ctx, data):
            return {"id": data.user_id, "name": data.body.name}, 201

        _, dispatcher = make_dispatcher(handler=undeclared)
        response = dispatcher.dispatch(self.request())
        self.assertEqual(response.status, 500)
        self.assertEqual(response.body["error"]["code"], "response_validation_error")

    def test_async_middleware_order(self):
        events = []

        async def middleware(ctx, call_next):
            events.append("before")
            result = await call_next(ctx)
            events.append("after")
            result.headers["X-Middleware"] = "yes"
            return result

        _, dispatcher = make_dispatcher(middleware=[middleware])
        response = asyncio.run(dispatcher.dispatch_async(self.request()))
        self.assertEqual(events, ["before", "after"])
        self.assertEqual(response.headers["X-Middleware"], "yes")

    def test_dispatch_rejects_running_event_loop(self):
        _, dispatcher = make_dispatcher()

        async def invoke():
            with self.assertRaisesRegex(RuntimeError, "dispatch_async"):
                dispatcher.dispatch(self.request())

        asyncio.run(invoke())


class RegistryTests(unittest.TestCase):
    def test_static_route_wins_over_dynamic_route(self):
        registry = ApiRegistry()

        @registry.route("/users/<str:name>", methods=["GET"])
        def dynamic(ctx, data):
            return "dynamic"

        @registry.route("/users/me", methods=["GET"])
        def static(ctx, data):
            return "static"

        dispatcher = Dispatcher(registry)
        response = dispatcher.dispatch(RequestContext("GET", "/users/me"))
        self.assertEqual(response.body, "static")

    def test_converter_and_method_not_allowed(self):
        registry = ApiRegistry()

        @registry.route("/objects/<uuid:object_id>", methods=["GET"])
        def view(ctx, data):
            self.assertIsInstance(ctx.path_params["object_id"], UUID)
            return ResponseContext(status=204)

        dispatcher = Dispatcher(registry)
        object_id = "123e4567-e89b-12d3-a456-426614174000"
        self.assertEqual(dispatcher.dispatch(RequestContext("GET", f"/objects/{object_id}")).status, 204)
        rejected = dispatcher.dispatch(RequestContext("POST", f"/objects/{object_id}"))
        self.assertEqual(rejected.status, 405)
        self.assertEqual(rejected.headers["Allow"], "GET")

    def test_ambiguous_routes_fail_at_compile_time(self):
        registry = ApiRegistry()

        @registry.route("/users/<int:first>", methods=["GET"])
        def first(ctx, data):
            return None

        @registry.route("/users/<int:second>", methods=["GET"])
        def second(ctx, data):
            return None

        with self.assertRaisesRegex(ValueError, "Ambiguous"):
            registry.compile()

    def test_registry_is_immutable_after_compile(self):
        registry = ApiRegistry().compile()
        with self.assertRaises(RuntimeError):
            registry.route("/late", methods=["GET"])


class OpenApiTests(unittest.TestCase):
    def test_document_uses_runtime_contract(self):
        registry, _ = make_dispatcher()
        document = generate_openapi(registry, title="Example", version="1")
        operation = document["paths"]["/users/{user_id}"]["patch"]
        self.assertEqual(operation["operationId"], "update_user")
        self.assertEqual(operation["parameters"][0]["in"], "path")
        self.assertIn("requestBody", operation)
        self.assertIn("200", operation["responses"])


class LegacyMigrationTests(unittest.TestCase):
    def test_conf_is_copied_and_uses_documented_precedence(self):
        from api_shop.legacy import dispatcher_from_conf

        class Handler:
            def post(self, request, data):
                return {"id": data.item_id, "name": data.name}

        conf = [
            {
                "url": "items/<int:item_id>",
                "class": Handler,
                "name": "items",
                "methods": {
                    "POST": [
                        {"name": "item_id", "type": int, "required": True},
                        {"name": "name", "type": str, "required": True, "min": 2},
                    ]
                },
            }
        ]
        with self.assertWarns(DeprecationWarning):
            dispatcher = dispatcher_from_conf(conf)
        response = dispatcher.dispatch(
            RequestContext(
                "POST",
                "/items/4",
                query={"name": "query"},
                body={"name": "body"},
            )
        )
        self.assertEqual(response.body, {"id": 4, "name": "body"})
        self.assertIs(conf[0]["methods"]["POST"][0]["type"], int)


if __name__ == "__main__":
    unittest.main()
