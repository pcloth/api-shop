from django.urls import path,re_path

from . import views

from src.api_shop import ApiShop, Api
from src.api_shop import data_format


conf = [
    {
        'url': 'login',
        'class': 'business_code.views.api_login',
        'name': '账户登录',
        'methods': {
            'POST': [
                {'name': 'username', 'type': data_format.regex(
                    r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$',name='邮箱'), 'required': True, 'min': 3, 'max': 24, 'description': '用户名'},
                {'name':'password', 'type': data_format.idcard, 'required': True, 'description': '密码'},
            ]
        }
    },
    {
        'url': ['test/alkdjflasjdf/aljdfalf','test2','three/user'],
        'class': 'business_code.views.test',
        'name': '测试数据',
        'methods': {
            'POST': [
                {'name':'add', 'type': str, 'required': True, 'min': 3, 'max': 24, 'description': '地址'},
                {'name':'bb', 'type': int, 'required': True, 'min': 0, 'max': 100, 'description': '百分比','default':95},
                {'name':'list', 'type': list, 'description': '列表'},
            ],
            'DELETE':[
                {'name':'id', 'type': int, 'required': True, 'min': 1,'description': '编号'},
            ]
        }
    },

]

af = ApiShop(conf, {
    'framework': 'django',
    'lang': 'zh'
})

app_name = 'api'
from src.api_shop import get_api_result_json


urlpatterns = [
    path('api_data', af.get_api_data, name='api_data'),
    path('document/', af.render_documents, name='document'),
    re_path(r'([\s\S]*)', af.api_entry, name='index')
]

