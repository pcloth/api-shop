# api-shop

> What is api-shop: Provides an easy-to-use, lightweight restful-api interface toolkit based on the django or flask framework.

## **demo Image**

![demo](/static/demo.png)


## **core function:**
1. Configuration api generation.
2. Automatically verify the data submitted by the request and convert it to a format.
3. Automatically generate api documents and provide a web page for query and mock data presentation.
4. Compatible with django and flask
5. Container format conversion, data_format.datetime format conversion class; '2019-01-18 23:25:25' to datetime
6. Custom Format Converter
7. Multi-language support.


## **update record:**
> 2019-01-23
>
> ver 1.6.0
>

- Add multi-language support, you can specify the language or extend the language pack in options.
- Document improvement
   


## **Usage: **
1. Installation:
```sh
Sudo pip install api-shop
```

2. Introduce:
```python
From api_shop from ApiShop, Api, data_format
```

Module Name | Function Description | Module Introduction
:----------- | :-----------: | :-----------
ApiShop | api initialization class | to load conf and options
Api | Business Inheritance Class | Used to inherit the actual business code after writing


3. Initialization
``` python
Conf = [
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
Url | str | url address of the interface, only need to fill in the relative address
Class | str,class | The business class that the interface actually calls (inherited to Api), which can be an object or a reference address
Name | str | the name of the interface
Methods | dict | methods that the interface can receive: GET POST DELETE PUT PATCH

> methods configuration instructions
>
Key | Value Type | Description
:----------- | :----------- | -----------:
Name | str | parameter name, received in data.name
Type | class | str, int, float, bool, list, dict, tuple, etc., also supports the data_format.datetime time format, you can also customize a type converter
Required | bool | Is it necessary?
Default | str | When not received, the default value, note that it will also be converted by the type converter specified by type.
Min | int,str | The minimum/minimum length, which is a string, is converted by the type converter specified by type.
Max | int,str | Maximum/maximum length, when a string is converted by the type converter specified by type.
Description | str | Description of the function, to see the contents of the document for the front-end personnel

4. Configuration
```python
Options = {
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
Base_url | str | /api/ | interface url prefix
Bad_request | bool | True | If the request is not valid, return it as a bad request; otherwise it is all 200 return
Document | str(path) |  | The path to the html template of the document page, there will be a simple template by default
Lang | str | en | Multi-language support, currently built in en, zh
Lang_pack | dict | None | Extended language pack if you want api-shop to support more languages

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

Custom format converter
```python
# When using a custom format converter, min and max will also automatically load this converter for comparison.
From datetime import datetime as dt
Class datetime():
    '''Converts str to datetime format '''
    Def __new__(self, string):
        If ':' in string:
            Return dt.strptime(string, '%Y-%m-%d %H:%M:%S')
        Else:
            Return dt.strptime(string, '%Y-%m-%d')
```

## example

1. [Django example] (https://github.com/pcloth/api-shop/tree/master/django_demo)
```python
## urls.py
From api_shop import ApiShop

## Interface Configuration Data
Conf = [
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

Options = {
            'base_url': '/api/', #base url, used to combine the front end api url can be default
            # 'document':BASE_DIR+'/api_shop/static/document.html', #Document routing rendering template Default
            'bad_request': True, # parameter bad_request If true, an error is returned to the front end, otherwise it returns a response of 200, which is accompanied by status=error and msg with error message.
        }


Ap = ApiShop(conf,options)

App_name='api'

Urlpatterns = [
    Path('api_data', ap.get_api_data, name='api_data'), # api document required interface
    Path('document/', ap.render_documents, name='document'), #apidocument rendered route
    Re_path(r'([\s\S]*)', ap.api_entry, name='index') # Take over all other routes from api/ below to api_entry entry method
]

```

###
```python
## account/views.py
From api_shop from Api

Class api_login(Api):
    Def post(self,request,data=None):
        '''api login interface, convenient WeChat user binding account '''
        Username = data.username
        Password = data.password
        User = authenticate(username=username, password=password)
        If user:
            Login(request, user)
            Token = TokenBackend.make_token(user).decode('utf-8')
            Return JsonResponse({'status': 'success', 'msg': 'execution success', 'token': token})
        
        Return JsonResponse({'status': 'error', 'msg': 'User login failed'})
```



2. [flask example] (https://github.com/pcloth/api-shop/tree/master/flask_demo)
```python
From flask import Flask,request,render_template_string

From werkzeug.routing import BaseConverter

From api_shop import ApiShop,Api

Class RegexConverter(BaseConverter):
    Def __init__(self, map, *args):
        Self.map = map
        Self.regex = args[0]

App = Flask(__name__)
# If using a blueprint, adding a regular processor must be used before registering the blueprint.
App.url_map.converters['regex'] = RegexConverter

Conf = [
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

Af = ApiShop(conf)

@app.route('/api/<regex("([\s\S]*)"):url>',methods=['GET', 'POST','PUT','DELETE','PATCH '])
Def hello_world(url):
    Print(url)
    If url=='document/':
        Return af.render_documents(request,url)
    If url=='api_data':
        Return af.get_api_data(request,url)

    Return af.api_entry(request,url)

If __name__ == '__main__':
    App.run(host="0.0.0.0",debug=True)
```
