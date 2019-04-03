# api-shop

> ### api-shop: An easy-to-use, fast restful-api interface toolkit compatible with `django` / `flask` / `bottle`.
> ### `All is for less overtime. `

## **demo Image**

![demo](/static/demo.png)


## **core function:**
1. Configuration api generation.
2. Automatically verify the data submitted by the request and convert it to the specified format, supporting: int, float, list, dict, set, tuple, bool
3. Automatically generate api documents and provide a web page for query and mock data presentation.
4. Compatible with `django` , `flask` , `bottle` (if you don't specify a frame, the frame is recognized by default in this order)
5. Automatically generate the interface `skeleton file` function (please open it carefully).
6. Custom format converter, data_format.datetime format conversion class; '2019-01-18 23:25:25' to datetime
7. Multi-language support, also supports custom language packs.
8. The documentation supports hot overloading.
9. The default value supports method functions.
10. Support url contains parameters, such as ```/api/user/<id>```, and set its rules when configuring the parameters parameter.
11. Support multiple url binding an interface


## **update record:**
> 2019-04-03
>
> var 1.7.3
- Added support for multiple interfaces to support multiple url bindings.
```python
{
         'url': ['weixin', 'weixin/<name>/<id>'],
         'class': 'business_code.views.test',
         'name': 'Account login',
         'methods': {
             'POST': [
                 {'name': 'id', 'type': bool, 'required': True, 'description': 'user id'},
                 {'name': 'name', 'type': str, 'min':4,'required': True,'description': 'username'},
             ],
         }
     },
```


> 2019-03-15
>
> ver 1.7.2
- Further abstract optimization code to facilitate the addition of new framework support.
- Added support for the bottle frame.
- Add the bad_request_error_status parameter. When bad_request==False, bad_request_error_status is the custom error status information returned to the bad request.


> 2019-03-14
>
> ver 1.7.1
- Optimize the framework loading logic, the default loading framework order ```django``` -> ```flask```; add configuration parameters directly to specify the framework.
- Optimize some of the regular processing logic.


> 2019-03-12
>
> ver 1.7.0
- Added automatic generation of interface skeleton files based on configuration files: When you add conf content, api-shop will automatically create based on its contents.Reduce the amount of code by cataloging files, importing modules, creating classes and methods, and creating notes based on parameters configured by the interface.
- E.g:
```python
Af = ApiShop(conf,
    {
        'lang': 'zh',
        'name_classification': ['WeChat', 'Account'],
        'url_classification': ['weixin', 'login'],
        'auto_create_folder': True, # Create folder automatically
        'auto_create_file': True, # Automatically create files
        'auto_create_class': True, # automatically create class
        'auto_create_method': True, # automatic creation method
    })
```

Generated file
```python
# api-shop automatically inserts code
from api_shop import Api


class api_login(Api):
    """WeChat account login """
    Pass
    Def post(self, request, data):
        """ todo:
        Api-shop automatically inserts code
        Data.username # username
        Data.ddd # Date
        """
        Pass
```

> 2019-03-06
>
> ver 1.6.7
- Add url parameter support
- E.g:
```python
Conf = [{
         'url': 'weixin/<name>/<id>',
         'class': 'business_code.views.test',
         'name': 'test api',
         'methods': {
            
             'POST': [
                 {'name': 'id', 'type': int, 'required': True, 'description': 'user id'},
                 {'name': 'name', 'type': str, 'min':4,'required': True,'description': 'username'},
             ],
         }
     },]
```

> 2019-02-25
>
> ver 1.6.5
- Add empty Response support, Api method can not return any value
- Added support for bool parameter types
- Interface documentation supports filtering (options are required)
   

## **Usage: **
1. Installation:
```sh
sudo pip install api-shop
```

2. Introduce:
```python
from api_shop from ApiShop, Api, data_format
```

Module Name | Function Description | Module Introduction
:----------- | :-----------: | :-----------
ApiShop | api initialization class | to load conf and options
Api | Business Inheritance Class | Used to inherit the actual business code after writing


3. Initialization
``` python
conf = [
    {
        'url': 'login',
        'class': 'account.views.api_login',
        'name': 'Account login',
        'methods': {
            'POST': [
                {'name':'username', 'type': str, 'required': True, 'min': 3, 'max': 24, 'description': 'username'},
                {'name':'password', 'type': str, 'required': True, 'min': 3, 'max': 24, 'description': 'password'},
            ],
            'GET':[]
        }
    },
]

```
> conf configuration instructions
>
Key | Value Type | Description
:----------- | :----------- | -----------:
url | str,list | The url address of the interface only needs to fill in the relative address. If there are multiple urls, you can configure it as `list`. Support url parameter: `/api/url/<id>`
class | str,class | The business class that the interface actually calls (inherited to Api), which can be an object or a reference address
name | str | the name of the interface
Methods | dict | methods that the interface can receive: GET POST DELETE PUT PATCH

> methods configuration instructions
>
Key | Value Type | Description
:----------- | :----------- | -----------:
name | str | parameter name, received in data.name
type | class | str, int, float, bool, list, dict, tuple, etc., also supports the data_format.datetime time format, you can also customize a type converter
required | bool | Is it necessary?
default | str,function | When not received, the default value, note that it will also be converted by the type converter specified by type.When it is a function, if it does not receive the request parameter, it will automatically run this method to get the value, and will not perform type conversion.
min | int,str | The minimum/minimum length, which is a string, is converted by the type converter specified by type.
max | int,str | Maximum/maximum length, when a string is converted by the type converter specified by type.
description | str | Description of the function, to see the contents of the document for the front-end personnel

4. Configuration
```python
options = {
                'base_url': '/api/',
                'bad_request': True,
                'document': BASE_DIR + '/api_shop/static/document.html',
                'lang': 'en',
                'lang_pack':{}
            }
```
> options configuration instructions


Key | Type | default | Description
:----------- | :----------- | :----------- | -----------:
base_url | str | /api/ | interface url prefix
bad_request | bool | True | If the request is not valid, return it as a bad request; otherwise it is all 200 return
bad_request_error_status | str, int, bool | 'error' | If the bad_request parameter is set to False, then this parameter will be enabled and will be accompanied by a status='error' message in the bad request. You can customize this information.
document | str(path) |  | The path to the html template of the document page, there will be a simple template by default
lang | str | en | Multi-language support, currently built in en, zh
lang_pack | dict | None | Extended language pack if you want api-shop to support more languages
name_classification | list | none | used for default document templates to filter interface names for easy searching
url_classification | list | None | Used by the default document template to filter the interface url for easy searching. Example: 'url_classification':['weixin', 'login']
auto_create_folder | bool | False | Automatically create folder
auto_create_file | bool | False | Automatically create files
auto_create_class | bool | False | Automatically create class
auto_create_method | bool | False | Automatically create method
Framework | str | None | Manually specify the framework, currently supports django, flask, bottle, if not specified, the framework will be identified in order, if multiple frames are installed at the same time, please specify manually.




> lang_pack language pack
>
> value is the target language
```python
'lang_pack':{
    'zh': {
            'no attributes found': '没有找到属性：',
            'not found in conf': '在conf参数中没找到方法: ',
            'no such interface': '没有这个接口',
            'is required': '是必要的',
            'parameter': '参数',
            'can not be empty': '不能为空',
            'must be type': '必须是类型',
            'minimum length': '最小长度',
            'minimum value': '最小值',
            'maximum length': '最大长度',
            'maximum value': '最大值',
            'The wrong configuration, methons must be loaded inside the list container.': '错误的配置，methons必须装的list容器内。',
            'no such interface method': '这个接口没有这个method',
            'Framework version is not compatible.': 'api-shop不支持当前框架版本。',
            'Not support': '不支持',
            'supported framework as follows:': '支持的框架如下：',
            'Did not find the framework':'没找指定的框架，请安装',
        }
}
```

custom format converter
```python
# When using a custom format converter, min and max will also automatically load this converter for comparison.
from datetime import datetime as dt
class datetime():
    '''Converts str to datetime format '''
    def __new__(self, string):
        if ':' in string:
            return dt.strptime(string, '%Y-%m-%d %H:%M:%S')
        else:
            return dt.strptime(string, '%Y-%m-%d')
```

## example

1. [Django example] 
```python
## urls.py
from api_shop import ApiShop

## Interface Configuration Data
conf = [
    {
        'url': 'login',
        'class': 'account.views.api_login', # need to introduce the api class, inherited from the above API interface class
        'name': 'Account login',
        'methods': {
            'POST': [
                {'name':'username', 'type': str, 'required': True, 'min': 3, 'max': 24, 'description': 'username'},
                {'name':'password', 'type': str, 'required': True, 'min': 3, 'max': 24, 'description': 'password'},
            ]
            ## Here you can insert more methods, such as GET, DELETE, POST, PATCH
        }
    },
    ## Here you can insert more api interfaces

]

## api-shop parameter settings:

options = {
            'base_url': '/api/', #base url, used to combine the front end api url can be default
            # 'document':BASE_DIR+'/api_shop/static/document.html', #Document routing rendering template Default
            'bad_request': True, # parameter bad_request If true, an error is returned to the front end, otherwise it returns a response of 200, which is accompanied by status=error and msg with error message.
        }


ap = ApiShop(conf,options)

app_name='api'

urlpatterns = [
    path('api_data', ap.get_api_data, name='api_data'), # api document required interface
    path('document/', ap.render_documents, name='document'), #apidocument rendered route
    re_path(r'([\s\S]*)', ap.api_entry, name='index') # Take over all other routes from api/ below to api_entry entry method
]

```

###
```python
## account/views.py
from api_shop from Api

class api_login(Api):
    def post(self,request,data=None):
        '''api login interface, convenient WeChat user binding account '''
        username = data.username
        password = data.password
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            token = TokenBackend.make_token(user).decode('utf-8')
            return {'status': 'success', 'msg': 'execution success', 'token': token}
        
        return {'status': 'error', 'msg': 'User login failed'},400
```



2. [flask example] 
```python
from flask import Flask,request,render_template_string

from werkzeug.routing import BaseConverter

from api_shop import ApiShop,Api

class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]

app = Flask(__name__)
# If using a blueprint, adding a regular processor must be used before registering the blueprint.
app.url_map.converters['regex'] = RegexConverter

conf = [
    {
        'url': 'login',
        'class': 'api.views.api_login',
        'name': 'Account login',
        'methods': {
            'POST': [
                {'name':'username', 'type': str, 'required': True, 'min': 3, 'max': 24, 'description': 'username'},
                {'name':'password', 'type': str, 'required': True, 'min': 3, 'max': 24, 'description': 'password'},
            ]
        }
    },
    {
        'url': 'test',
        'class': 'api.views.test',
        'name': 'test data',
        'methods': {
            'GET':[{'name':'bb', 'type': int, 'required': True, 'min': 0, 'max': 100, 'description': 'percent', 'default': 95},],
            'POST': [
                {'name':'add', 'type': str, 'required': True, 'min': 3, 'max': 24, 'description': 'address'},
                {'name':'bb', 'type': int, 'required': True, 'min': 0, 'max': 100, 'description': 'percent', 'default': 95},
                {'name':'list', 'type': list, 'description': 'list'},
            ],
            'DELETE':[
                {'name':'id', 'type': int, 'required': True, 'min': 1, 'description': 'number'},
            ]
        }
    },

]

af = ApiShop(conf)

@app.route('/api/<regex("([\s\S]*)"):url>',methods=['GET', 'POST','PUT','DELETE','PATCH '])
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




3. [bottle例子]
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


