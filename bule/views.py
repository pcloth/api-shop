

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
import sys
sys.path.insert(0, "D:\\codes\\api-shop")
from api_shop import ApiShop, Api, data_format
from flask import request

simple_page = Blueprint('simple_page', __name__,
                        template_folder='templates')


@simple_page.route('/', defaults={'page': 'index'})
@simple_page.route('/<page>')
def show(page):
    try:
        return render_template('pages/%s.html' % page)
    except TemplateNotFound:
        abort(404)
from api.views import api_login

conf = [
    {
        'url': 'login',
        'class': api_login,#'api.views.api_login',
        'name': '账户登录',
        'methods': {
            'POST': [
                {'name': 'username', 'type': str, 'required': True,
                    'min': 3, 'max': 24, 'description': '用户名'},
                {'name': 'ddd', 'type': str,  'min': 20,'max': 6, 'description': '日期'},
            ]
        }
    },
    {
        'url': 'test',
        'class': 'api.views.test',
        'name': '账户登录',
        'methods': {
            'POST': [
                {'name': 'username', 'type': str, 'required': True,
                    'min': 3, 'max': 24, 'description': '用户名'},
                {'name': 'ddd', 'type': data_format.datetime, 'required': False, 'min': '2018-01-01',
                    'max': '2019-01-01', 'description': '日期', 'default': '2018-05-05'},
            ],
            'DELETE':[{'name': 'id', 'type': int, 'required': True,
                    'min': 3, 'max': 24, 'description': '用户id'},],
            # 'GET':[{'name': 'id', 'type': int, 'required': True,
            #         'min': 3, 'max': 24, 'description': '用户id'},]
        }
    },


]


af = ApiShop(conf,{'lang':'zh'})

print(af.url_dict)

@simple_page.route('/api/<regex("([\s\S]*)"):url>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def hello_world(url):
    print(url)
    if url == 'document/':
        return af.render_documents(request, url)
    if url == 'api_data':
        return af.get_api_data(request, url)

    return af.api_entry(request, url)
