"""OpenAPI 3.0 generation for api-shop configuration."""

import inspect
import re


PATH_PARAMETER_RE = re.compile(
    r"<(?:[A-Za-z_][A-Za-z0-9_]*(?:\([^>]*\))?:)?"
    r"([A-Za-z_][A-Za-z0-9_]*)>"
)

TYPE_SCHEMAS = {
    "str": {"type": "string"},
    "int": {"type": "integer"},
    "float": {"type": "number"},
    "complex": {"type": "number"},
    "bool": {"type": "boolean"},
    "dict": {"type": "object"},
    "list": {"type": "array", "items": {}},
    "set": {"type": "array", "items": {}, "uniqueItems": True},
    "tuple": {"type": "array", "items": {}},
}


def _type_name(value):
    if isinstance(value, str):
        return value.rsplit('.', 1)[-1]
    return getattr(value, '__name__', value.__class__.__name__)


def _schema(parameter):
    type_name = _type_name(parameter.get('type', str))
    schema = dict(TYPE_SCHEMAS.get(type_name, {'type': 'string'}))
    if parameter.get('options') is not None:
        schema['enum'] = list(parameter['options'])
    default = parameter.get('default')
    if default is not None and not callable(default):
        schema['default'] = default

    is_number = schema.get('type') in ('integer', 'number')
    is_container = schema.get('type') in ('array', 'object')
    if parameter.get('min') is not None:
        key = 'minimum' if is_number else ('minItems' if is_container else 'minLength')
        schema[key] = parameter['min']
    if parameter.get('max') is not None:
        key = 'maximum' if is_number else ('maxItems' if is_container else 'maxLength')
        schema[key] = parameter['max']
    if type_name not in TYPE_SCHEMAS:
        schema['x-python-type'] = type_name
    return schema


def _clean_document(value):
    if not value:
        return None
    document = inspect.cleandoc(str(value)).strip()
    return document or None


def _document_summary(document):
    if not document:
        return None
    return next(
        (line.strip() for line in document.splitlines() if line.strip()),
        None,
    )


def _operation(method, parameters, path_names, operation_id):
    operation = {
        'operationId': operation_id,
        'parameters': [],
        'responses': {'200': {'description': 'Successful response'}},
    }
    properties = {}
    required = []
    query_method = method in ('GET', 'DELETE', 'HEAD', 'OPTIONS')

    for parameter in parameters:
        name = parameter['name']
        schema = _schema(parameter)
        description = parameter.get('description')
        if name in path_names or query_method:
            item = {
                'name': name,
                'in': 'path' if name in path_names else 'query',
                'required': True if name in path_names else bool(parameter.get('required')),
                'schema': schema,
            }
            if description:
                item['description'] = description
            operation['parameters'].append(item)
        else:
            properties[name] = dict(schema)
            if description:
                properties[name]['description'] = description
            if parameter.get('required'):
                required.append(name)

    documented_path_names = {
        item['name'] for item in operation['parameters']
        if item['in'] == 'path'
    }
    for name in sorted(path_names - documented_path_names):
        operation['parameters'].append({
            'name': name,
            'in': 'path',
            'required': True,
            'schema': {'type': 'string'},
        })

    if properties:
        body_schema = {'type': 'object', 'properties': properties}
        if required:
            body_schema['required'] = required
        operation['requestBody'] = {
            'required': bool(required),
            'content': {'application/json': {'schema': body_schema}},
        }
    return operation


def generate_openapi(conf, title='api-shop API', version='1.0.0',
                     description=None, base_url=None):
    '''从 ApiShop conf 生成 OpenAPI 3.0.3 文档。'''
    document = {
        'openapi': '3.0.3',
        'info': {'title': title, 'version': str(version)},
        'paths': {},
        'tags': [],
    }
    if description:
        document['info']['description'] = description
    if base_url:
        document['servers'] = [{'url': base_url}]

    tag_names = set()
    tag_groups = {}
    tag_group_by_name = {}

    for endpoint in conf:
        urls = endpoint.get('url', [])
        if isinstance(urls, str):
            urls = [urls]
        for configured_path in urls:
            path_names = set(PATH_PARAMETER_RE.findall(configured_path))
            path = PATH_PARAMETER_RE.sub(r'{\1}', configured_path)
            if not path.startswith('/'):
                path = '/' + path

            tag_name = str(endpoint.get('name') or path)
            endpoint_document = _clean_document(endpoint.get('document'))
            if tag_name not in tag_names:
                tag = {'name': tag_name}
                if endpoint_document:
                    tag['description'] = endpoint_document
                document['tags'].append(tag)
                tag_names.add(tag_name)

            module_name = path.strip('/').split('/', 1)[0] or 'root'
            if tag_name not in tag_group_by_name:
                tag_groups.setdefault(module_name, []).append(tag_name)
                tag_group_by_name[tag_name] = module_name

            path_item = document['paths'].setdefault(path, {})
            for method, parameters in endpoint.get('methods', {}).items():
                method = method.upper()
                operation_id = '{}_{}'.format(
                    method.lower(),
                    re.sub(r'[^A-Za-z0-9_]+', '_', path).strip('_') or 'root',
                )
                operation = _operation(method, parameters, path_names, operation_id)
                operation['tags'] = [tag_name]

                method_documents = endpoint.get('methods_documents', {})
                method_document = _clean_document(
                    method_documents.get(method)
                    or method_documents.get(method.lower())
                )
                if method_document:
                    operation['summary'] = _document_summary(method_document)
                    operation['description'] = method_document
                else:
                    operation['summary'] = '{} - {}'.format(tag_name, method)
                    if endpoint_document:
                        operation['description'] = endpoint_document
                path_item[method.lower()] = operation

    if tag_groups:
        document['x-tagGroups'] = [
            {'name': group_name, 'tags': group_tags}
            for group_name, group_tags in tag_groups.items()
        ]
    return document
