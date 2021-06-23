# 快速上手
![PyPI](https://img.shields.io/pypi/v/api-shop?logo=api-shop) ![PyPI - Downloads](https://img.shields.io/pypi/dm/api-shop)

## 安装
```sh
sudo pip install api-shop
```
## 引入
```python
from api_shop from ApiShop,Api,data_format
```
## api数据配置
``` python
conf = [
    {
        'url': 'login',
        'class': 'account.views.api_login',
        'name': '账户登录',
        'methods': {
            'POST': [
                {'name':'username', 'type': str, 'required': True, 'min': 3, 'max': 24, 'description': '用户名'},
                {'name':'password', 'type': str, 'required': True, 'min': 3, 'max': 24, 'description': '密码'},
            ],
            'GET':[]
        }
    },
]

```

### 接口配置说明

|键|类型| 说明 | 例子 |
|---|---|---|---|
|url| str/list | 接口访问的url，支持list包裹多个url，也支持<参数名>模式，url中添加<参数名>的话，方法参数列表中必须要包含该参数，并指定`required=True`| 'login','user/<id>|
|class| str/Class对象 | 为字符串时，是`Api接口继承对象`的路径，为对象时就是该`Api接口继承对象`| account.views.api_login |
|methods| dict | 这个对象包含了每个接口可以接受的方法和参数 | key可以为GET/POST/PUT/PATCH/PUT/DELETE等http支持的方法 |

#### methods配置说明
::: tips
单个methods的value为一个list对象，其中描述了该方法支持的参数
:::
|键|类型| 说明 | 例子 |
|---|---|---|---|
|name|str|参数名字| username|
|type|object| 参数类型，目前支持int，float，list，dict，set，tuple，bool，也支持自定义类型和其他可以被转换的类型 | 详情可以查看data_format扩展 |
|required|bool|是否必要参数，如果为True，用户请求中没有该参数将会被拦截|缺省为`False`|
|min|int|参数的最小值(int)或者最小长度(str/list/set/tuple)，用户提交小于或者短于这个值的参数，将会被拦截| 5 |
|max|int|参数的最大值(int)或者最大长度(str/list/set/tuple)，用户提交大于或者超过长度的参数，将会被拦截| 5 |
|default|`同类型参数`、`方法`、`类`| 比如type=int的一个参数，default=1的时候，用户如果不提交参数，将会自动填充1，如果default为一个方法或者类，将会自动填充`运行`/`实例化`结果||
|options|list|这是参数的可选项，用户提交的参数必须在可选项中，否则将会被拦截|options=['a','c'] 表示用户只能提交该参数的值为a或者c|
|description|str|参数的描述，用来给前端开发人员的参考说明||




## 例子

### django
``` python
ap = ApiShop(conf,options)

app_name='api'

urlpatterns = [
    path('api_data', ap.get_api_data, name='api_data'), # api文档需要的接口
    path('document/', ap.render_documents, name='document'), #api文档渲染的路由
    re_path(r'([\s\S]*)', ap.api_entry, name='index') # 接管api/下面其他的全部路由到api_entry入口方法
]
```

### flask
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


### bottle
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
