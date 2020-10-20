

from flask import Blueprint,  request

from src.api_shop import ApiShop, Api, data_format,ApiDataClass


simple_page = Blueprint('simple_page', __name__,
                        template_folder='templates')

conf = [
    {
        'url': 'weixin/login',
        'class': 'business_code.test.abc.api_login',
        'name': '微信账户登录',
        'methods': {
            'POST': [
                {'name': 'username', 'type': str, 'required': True, 'description': '用户名',},
                {'name': 'ddd', 'type': str,   'description': '日期','options':['2018-10-26']},
            ]
        }
    },
    {
        'url': ['weixin','weixin/<name>/<id>'],
        'class': 'business_code.views.test',
        'name': '账户登录',
        'methods': {
            'POST': [
                {'name': 'id', 'type': str, 'description': '用户id'},
                {'name': 'name', 'type': str, 'min': 4, 'required': True, 'description': '用户name'},
                {'name': 'a', 'type': str, 'description': '参数A'},
            ],
        }
    },


]


af = ApiShop(conf,
    {
        # 'lang': 'zh',
        'name_classification': ['微信', '账户'],
        'url_classification': ['weixin', 'login'],
        # 'auto_create_folder': True,  # 自动创建文件夹
        # 'auto_create_file': True,  # 自动创建文件
        # 'auto_create_class': True,  # 自动创建类
        'auto_create_method': True,  # 自动创建方法
        'framework': 'flask',
        # 'debug':False,
    })

from src.api_shop import get_api_result_json
from business_code.test.abc import api_login


@simple_page.route('/api/<regex("([\s\S]*)"):url>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def hello_world(url):
    if url == 'document/':
        return af.render_documents(request, url)
    if url == 'api_data':
        return af.get_api_data(request, url)

    return af.api_entry(request, url)
