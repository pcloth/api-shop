import sys
import types
import unittest
from unittest.mock import patch


flask = types.ModuleType('flask')
flask.render_template_string = lambda value: value
flask.jsonify = lambda value: value
sys.modules.setdefault('flask', flask)

import api_shop.api_shop as api_shop_module
from api_shop.api_shop import ApiShop, FW, SingleApiShop


class Handler:
    def get(self, request, data):
        return {'ok': True}


class DocumentedHandler:
    """商品管理。"""

    def get(self, request, data):
        """查询商品列表。

        返回符合筛选条件的商品。
        """

    def post(self, request, data):
        """创建商品。

        创建并返回新的商品记录。
        """


def make_conf(url='items/<int:id>'):
    return [{
        'url': url,
        'class': Handler,
        'name': 'items',
        'methods': {
            'GET': [
                {'name': 'id', 'type': int, 'required': True, 'min': 0},
            ],
        },
    }]


class MasterRegressionTests(unittest.TestCase):
    def setUp(self):
        api_shop_module.single_apishop = None

    def make_shop(self, conf=None, **options):
        options.setdefault('framework', 'flask')
        return ApiShop(conf or [], options)

    def test_framework_autodetection_stops_at_first_supported_framework(self):
        modules = {
            'django.http': types.SimpleNamespace(
                JsonResponse=object(), HttpResponse=object()),
            'flask': types.SimpleNamespace(
                render_template_string=object(), jsonify=object()),
            'bottle': types.SimpleNamespace(
                template=object(), HTTPResponse=object()),
        }
        with patch('api_shop.api_shop.importlib.import_module',
                   side_effect=lambda name: modules[name]):
            self.assertEqual(FW().name, 'django')

    def test_initialization_does_not_mutate_caller_config(self):
        conf = make_conf()
        self.make_shop(conf)
        self.assertIs(conf[0]['class'], Handler)
        self.assertIs(conf[0]['methods']['GET'][0]['type'], int)
        self.assertNotIn('methods_documents', conf[0])

    def test_handler_import_failure_still_terminates_service(self):
        conf = [{
            'url': 'broken', 'class': 'missing.module.Handler',
            'name': 'broken', 'methods': {},
        }]
        with patch('api_shop.api_shop.os._exit', side_effect=SystemExit) as exit_:
            with self.assertRaises(SystemExit):
                self.make_shop(conf, debug=False)
        exit_.assert_called_once_with(0)

    def test_autofill_options_are_no_longer_exposed(self):
        options = self.make_shop().options
        self.assertFalse(any(key.startswith('auto_create_') for key in options))

    def test_request_sources_are_merged_with_json_precedence(self):
        class Values:
            def __init__(self, values):
                self.values = values

            def __bool__(self):
                return bool(self.values)

            def to_dict(self):
                return dict(self.values)

        class Request:
            args = Values({'source': 'query', 'query': 'kept'})
            form = Values({'source': 'form', 'form': 'kept'})

            def get_json(self, silent=False):
                return {'source': 'json', 'body': 'kept'}

        data = self.make_shop().get_parameter(Request())
        self.assertEqual(data, {
            'source': 'json', 'query': 'kept',
            'form': 'kept', 'body': 'kept',
        })

    def test_zero_boundaries_and_boolean_values_are_validated(self):
        shop = self.make_shop()
        error, _ = shop.verify_parameter(
            None, [{'name': 'count', 'type': int, 'min': 0}],
            parameter={'count': -1})
        self.assertTrue(error)

        error, _ = shop.verify_parameter(
            None, [{'name': 'count', 'type': int, 'max': 0}],
            parameter={'count': 1})
        self.assertTrue(error)

        error, _ = shop.verify_parameter(
            None, [{'name': 'enabled', 'type': bool}],
            parameter={'enabled': 'not-a-bool'})
        self.assertTrue(error)

    def test_static_routes_win_and_converters_constrain_matches(self):
        conf = [
            {'url': 'users/<id>', 'class': Handler,
             'name': 'dynamic', 'methods': {'GET': []}},
            {'url': 'users/me', 'class': type('Static', (), {}),
             'name': 'static', 'methods': {'GET': []}},
        ]
        shop = self.make_shop(conf)
        model, key, _ = shop._ApiShop__find_api_function('users/me')
        self.assertEqual(model.__name__, 'Static')
        self.assertEqual(key, 'users/me')

        integer_shop = self.make_shop(make_conf('objects/<int:id>'))
        model, key, values = integer_shop._ApiShop__find_api_function(
            'objects/not-an-int')
        self.assertIsNone(key)
        self.assertIsNone(values)

    def test_singleton_read_does_not_reset_it_and_force_is_supported(self):
        first = SingleApiShop(make_conf(), {'framework': 'flask'})
        same = SingleApiShop()
        self.assertIs(same, first)
        self.assertEqual(len(same.conf), 1)

        replacement = SingleApiShop([], {'framework': 'flask'}, force=True)
        self.assertIsNot(replacement, first)
        self.assertEqual(replacement.conf, [])

    def test_missing_document_keeps_fallback_page(self):
        shop = self.make_shop(document='/definitely/missing/document.html')
        self.assertIn(
            'document template not found', shop.render_documents(None).lower())

    def test_default_document_uses_scalar_and_openapi_route(self):
        document = self.make_shop().render_documents(None)
        self.assertIn('Scalar.createApiReference', document)
        self.assertIn('../openapi.json', document)
        self.assertIn('../_api_shop/scalar-1.68.0.js', document)
        self.assertNotIn('cdn.jsdelivr.net', document)
        self.assertNotIn('SwaggerUIBundle', document)

    def test_scalar_asset_is_served_locally_with_immutable_cache(self):
        shop = self.make_shop()
        body, status, headers = shop.api_entry(
            object(), '_api_shop/scalar-1.68.0.js')

        self.assertEqual(status, 200)
        self.assertGreater(len(body), 3_000_000)
        self.assertTrue(body.startswith(b'(function()'))
        self.assertEqual(
            headers['Content-Type'],
            'application/javascript; charset=utf-8')
        self.assertEqual(
            headers['Cache-Control'],
            'public, max-age=31536000, immutable')

    def test_legacy_document_data_returns_migration_notice(self):
        shop = self.make_shop(make_conf(), lang='zh')
        payload, status = shop.get_api_data(None)

        self.assertEqual(status, 410)
        self.assertEqual(payload['status'], 'gone')
        self.assertEqual(payload['replacement'], 'get_openapi_data')
        self.assertIn('已移除', payload['message'])
        self.assertNotIn('data', payload)
        self.assertNotIn('options', payload)

    def test_openapi_document_matches_routes_and_constraints(self):
        document = self.make_shop(make_conf()).get_openapi_schema(
            title='Example', version='1.2.3')
        operation = document['paths']['/items/{id}']['get']
        self.assertEqual(document['openapi'], '3.0.3')
        self.assertEqual(document['info']['title'], 'Example')
        self.assertEqual(operation['tags'], ['items'])
        self.assertEqual(document['x-tagGroups'], [
            {'name': 'items', 'tags': ['items']},
        ])
        self.assertEqual(operation['parameters'][0]['in'], 'path')
        self.assertEqual(operation['parameters'][0]['schema']['minimum'], 0)

    def test_openapi_always_declares_templated_path_parameters(self):
        conf = [{
            'url': 'health/<probe>', 'class': Handler,
            'name': 'health', 'methods': {'GET': []},
        }]
        operation = self.make_shop(conf).get_openapi_schema()[
            'paths']['/health/{probe}']['get']
        self.assertEqual(operation['parameters'], [{
            'name': 'probe', 'in': 'path', 'required': True,
            'schema': {'type': 'string'},
        }])

    def test_openapi_groups_methods_and_uses_method_docstrings(self):
        conf = [{
            'url': 'products',
            'class': DocumentedHandler,
            'name': '商品功能',
            'methods': {'GET': [], 'POST': []},
        }]
        document = self.make_shop(conf).get_openapi_schema()
        get_operation = document['paths']['/products']['get']
        post_operation = document['paths']['/products']['post']

        self.assertEqual(get_operation['tags'], ['商品功能'])
        self.assertEqual(post_operation['tags'], ['商品功能'])
        self.assertEqual(get_operation['summary'], '查询商品列表。')
        self.assertEqual(post_operation['summary'], '创建商品。')
        self.assertIn('返回符合筛选条件的商品。',
                      get_operation['description'])
        self.assertEqual(document['tags'], [{
            'name': '商品功能', 'description': '商品管理。',
        }])
        self.assertEqual(document['x-tagGroups'], [{
            'name': 'products', 'tags': ['商品功能'],
        }])


if __name__ == '__main__':
    unittest.main()
