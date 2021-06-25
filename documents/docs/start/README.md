# 快速上手
## 安装
```sh
sudo pip install api-shop
```
## 引入
```python
from api_shop from ApiShop,Api,data_format
```
## ApiShop 初始化
``` python
from api_shop import ApiShop
conf = [
    {
        'url': 'user',
        'class': 'account.api_class.UserApi',
        'name': '账户接口',
        'methods': {
            'POST': [
                {'name':'username', 'type': str, 'required': True, 'min': 3, 'max': 24, 'description': '用户名'},
                {'name':'password', 'type': str, 'required': True, 'min': 3, 'max': 24, 'description': '密码'},
            ],
            'GET':[]
        }
    },
]

options = {
    'lang': 'zh',
}

af = ApiShop(conf,options)

```

### 例子

#### django
``` python
ap = ApiShop(conf,options)

app_name='api'

urlpatterns = [
    path('api_data', ap.get_api_data, name='api_data'), # api文档需要的接口
    path('document/', ap.render_documents, name='document'), #api文档渲染的路由
    re_path(r'([\s\S]*)', ap.api_entry, name='index') # 接管api/下面其他的全部路由到api_entry入口方法
]
```

#### flask
``` python
from flask import Flask,request,render_template_string

from werkzeug.routing import BaseConverter

from api_shop import ApiShop,Api

class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]

app = Flask(__name__)
# 如果使用蓝图，添加正则处理器必须是在注册蓝图之前使用。
app.url_map.converters['regex'] = RegexConverter

conf = [
    {
        'url': 'login',
        'class': 'api.views.api_login',
        'name': '账户登录',
        'methods': {
            'POST': [
                {'name':'username', 'type': str, 'required': True, 'min': 3, 'max': 24, 'description': '用户名'},
                {'name':'password', 'type': str, 'required': True, 'min': 3, 'max': 24, 'description': '密码'},
            ]
        }
    },
    {
        'url': 'test',
        'class': 'api.views.test',
        'name': '测试数据',
        'methods': {
            'GET':[{'name':'bb', 'type': int, 'required': True, 'min': 0, 'max': 100, 'description': '百分比','default':95},],
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
```


#### bottle
```python
from bottle import route, run, template, request,HTTPResponse
from src.api_shop import ApiShop

conf = [
    {
        'url': 'weixin/login',
        'class': 'business_code.test.abc.api_login',
        'name': '微信账户登录',
        'methods': {
            'POST': [
                {'name': 'username', 'type': str, 'required': True,
                    'min': 3, 'max': 24, 'description': '用户名'},
                {'name': 'ddd', 'type': str,   'description': '日期'},
            ]
        }
    },
    {
        'url': 'weixin/<name>/<id>',
        'class': 'business_code.views.test',
        'name': '账户登录',
        'methods': {
            
            'POST': [{'name': 'id', 'type': bool, 'required': True,
                         'description': '用户id'},
                         {'name': 'name', 'type': str, 'min':4,'required': True,
                         'description': '用户name'}, 
                    ],
        }
    },
]

af = ApiShop(conf,
    {
        'lang': 'zh',
        'name_classification': ['微信', '账户'],
        'url_classification': ['weixin', 'login'],
        'framework':'bottle'
    })


@route('/api/<url:re:([\s\S]*)>',['GET','PUT','PATCH','DELETE','POST'])
def api_index(url):
    print('*'*20,url)
    if url == 'document/':
        return af.render_documents(request, url)
    if url == 'api_data':
        return af.get_api_data(request, url)
    return af.api_entry(request, url)

run(host='localhost', port=8080,reloader=True,debug=True)
```


## Api接口业务
::: tip Api类
我们提供了一个Api类，用来封装你的业务代码
:::

```python
from api_shop import Api

class UserApi(Api):
    '''这里是接口描述文档'''

    def get(self, request, data):
        '''查询用户'''
        return {'user_name': '测试用户'}

    def post(self, request, data):
        '''接受新增用户或者修改用户'''
        return {'status':'success'}

    def patch(self, request, data):
        '''这里是patch方法'''

    def delete(self, request, data):
        '''这里是删除方法'''
        return {'msg':'这是一个错误请求'}, 401

    def put(self, request, data):
        '''这里是put方法'''
```

### methods方法
我们提供了一个快速的构建methods方法接口，如上面的代码所示，类方法get、post、patch、delete、put各自代表了请求的method方法
1. 类方法中直接返回一个dict对象，就可以让用户收到一个json的response。
2. 如果需要返回非200的response，则需要在return中标识出来
