# api-shop

> What is api-shop: Provides an easy-to-use, lightweight restful-api interface toolkit based on the django or flask framework.

## **demo Image**

![demo](/static/demo.png)


## **core function:**
1. Configuration api generation.
2. Automatically verify the data submitted by the request and convert it to a format.
3. Automatically generate api documents and provide a web page for query and mock data presentation.
4. Compatible with django and flask
5. Container format conversion: list, dict, set, tuple
6. Custom Format Converter, data_format.datetime format conversion class; '2019-01-18 23:25:25' to datetime
7. Multi-language support.
8. Document support hot overload.
9. The default value supports method functions.


## **update record:**
> 2019-02-11
>
> ver 1.6.4
- Fixed a problem where the default value is int:0 and does not trigger.


> 2019-01-30
>
> ver 1.6.2
- Optimize project catalog
- Shorten the format converter type name
- The default value supports method functions, such as datetime.now. If it is a method function, it will no longer automatically compare types and conversions. You need to grasp the format yourself.

> 2019-01-29
>
> ver 1.6.1
- Document support hot overload.
- Document added version support
- Optimization error tips

> 2019-01-23
>
> ver 1.6.0
>

- Add multi-language support, you can specify the language or extend the language pack in options.
- Document improvement
   


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
url | str | url address of the interface, only need to fill in the relative address
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
document | str(path) |  | The path to the html template of the document page, there will be a simple template by default
lang | str | en | Multi-language support, currently built in en, zh
lang_pack | dict | None | Extended language pack if you want api-shop to support more languages

> lang_pack language pack
>
> value is the target language
```python
'lang_pack':{
    'en': {
            'django version error': 'Django version is not compatible',
            'not flask or django': 'Currently only compatible with django and flask',
            'no attributes found': 'No attributes found: ',
            'not found in conf': 'Not found in conf: ',
            'document template not found': 'Document template not found',
            'no such interface': 'No such interface',
            'is required': 'is required',
            'parameter': 'Parameter',
            'can not be empty': 'can not be empty',
            'must be type': 'must be type',
            'minimum length': 'minimum length',
            'minimum value': 'minimum value',
            'maximum length': 'maximum length',
            'maximum value': 'maximum value',
            'The wrong configuration, methons must be loaded inside the list container.': 'The wrong configuration, methons must be loaded inside the list container.',
            'no such interface method': 'No such interface method',
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
