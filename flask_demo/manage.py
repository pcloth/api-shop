from flask import Flask,request,render_template_string

from werkzeug.routing import BaseConverter

import sys
sys.path.insert(0,"D:\\codes\\api-shop")
from api_shop import ApiShop, Api, data_format
# from api_shop.data_format import datetime


class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]

app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter

conf = [
    {
        'url': 'login',
        'class': 'api.views.api_login',
        'name': '账户登录',
        'methods': {
            'POST': [
                {'name':'username', 'type': str, 'required': True, 'min': 3, 'max': 24, 'description': '用户名'},
                {'name':'ddd', 'type': data_format.datetime, 'required': False, 'min': '2018-01-01', 'max': '2019-01-01', 'description': '日期','default':'2018-05-05'},
            ]
        }
    },
    {
        'url': 'login/test',
        'class': 'api.views.api_login',
        'name': '账户登录',
        'methods': {
            'POST': [
                {'name':'username', 'type': str, 'required': True, 'min': 3, 'max': 24, 'description': '用户名'},
                {'name':'ddd', 'type': data_format.datetime, 'required': False, 'min': '2018-01-01', 'max': '2019-01-01', 'description': '日期','default':'2018-05-05'},
            ]
        }
    },
    

]


af = ApiShop(conf)



@app.route('/api/<regex("([\s\S]*)"):url>',methods=['GET', 'POST','PUT','DELETE','PATCH'])
def hello_world(url):
    print(url)
    if url=='document/':
        return af.render_documents(request,url)
    if url=='api_data':
        return af.get_api_data(request,url)

    return af.api_entry(request,url)

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)