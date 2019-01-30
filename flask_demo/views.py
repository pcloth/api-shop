

from flask import Blueprint,  request

from src.api_shop import ApiShop, Api, data_format


simple_page = Blueprint('simple_page', __name__,
                        template_folder='templates')

conf = [
    {
        'url': 'login',
        'class': 'business_code.views.api_login',
        'name': '账户登录',
        'methods': {
            'POST': [
                {'name': 'username', 'type': str, 'required': True,
                    'min': 3, 'max': 24, 'description': '用户名'},
                {'name': 'ddd', 'type': str,  'min': 20,
                    'max': 6, 'description': '日期'},
            ]
        }
    },
    {
        'url': 'test',
        'class': 'business_code.views.test',
        'name': '账户登录',
        'methods': {
            'POST': [
                {'name': 'username', 'type': str, 'required': True,
                    'min': 3, 'max': 24, 'description': '用户名'},
                {'name': 'ddd', 'type': data_format.datetime, 'required': False, 'min': '2018-01-01',
                    'max': '2019-01-01', 'description': '日期', 'default': data_format.datetime.now},
            ],
            'DELETE': [{'name': 'id', 'type': int, 'required': True,
                        'min': 3, 'max': 24, 'description': '用户id'}, ],
            # 'GET':[{'name': 'id', 'type': int, 'required': True,
            #         'min': 3, 'max': 24, 'description': '用户id'},]
        }
    },


]


af = ApiShop(conf, {'lang': 'zh'})


@simple_page.route('/api/<regex("([\s\S]*)"):url>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def hello_world(url):
    print(url)
    if url == 'document/':
        return af.render_documents(request, url)
    if url == 'api_data':
        return af.get_api_data(request, url)

    return af.api_entry(request, url)
