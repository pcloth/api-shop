# components

模块名字 | 功能description | 模块介绍
:----------- | :-----------: | :-----------
ApiShop         | Api initialization class        | Used to load conf and options
Api         | Business base class        | Used to inherit and write the actual business code
get_api_result_json         | Call the business class directly(It will be deleted in later versions)        | return json,status_code
get_api_result_response         | Call the business class directly(It will be deleted in later versions)        | return response
data_format | Built-in custom data format | data_format.datetime Convert a string to datetime format
data_format.DataExpansion | Custom data foundation class | Used to write custom data formats



## ApiShop Class component
::: tip
The api-shop core class, after instantiation, generates an interface object. You only need to access the instance method to call the corresponding business code.
:::


```python
ap = ApiShop(conf,options)
```


### Run another api interface directly in the code
::: tip
Starting from version 1.12.0, the ApiShop core class provides an api_run method to run another api code in the code for easy reuse.
This method will replace the original get_api_result_json and get_api_result_response
:::
```python
'''
     request is directly passed into the current request,
     url is the interface url you want to access
     If method is not passed in, it is = request.method
     parameter request parameter, if it is not passed, no parameter is passed to the api
     json returns json data by default True, False will return response
'''
response_json,code = ap.api_run(request, url, method='GET', parameter={'a':1}, json=True)
print(response_json,code)
```

### ApiShop conf description
#### ApiShop conf example
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

#### ApiShop conf description
Key | Value Type | Description
:----------- | :----------- | -----------:
url         | str,list        | The url address of the interface only needs to fill in the relative address. If there are multiple urls, you can configure it as `list`. Support url parameter: `/api/url/<id>`
class         | str,class        | The business class actually invoked by the interface (inherited to Api), which can be an object or a reference address.
name         | str        | Interface name
methods         | dict        | Methods that the interface can receive: GET POST DELETE PUT PATCH

### ApiShop conf methods description
#### ApiShop conf methods description
Key | Value Type | Description
:----------- | :----------- | -----------:
name | str | parameter name, received in data.name
type | class | str, int, float, bool, list, dict, tuple, etc., also supports the data_format.datetime time format, you can also customize a type converter
required | bool | Is it necessary?
default | str,function | When not received, the default value, note that it will also be converted by the type converter specified by type.When it is a function, if it does not receive the request parameter, it will automatically run this method to get the value, and will not perform type conversion.
min | int,str | The minimum/minimum length, which is a string, is converted by the type converter specified by type.
max | int,str | Maximum/maximum length, when a string is converted by the type converter specified by type.
description | str | Description of the function, to see the contents of the document for the front-end personnel
options | list | The value of the parameter must be in this list, for example: [1,4,7]. Receiving parameters outside this list will trigger bad_request


### ApiShop options description
#### ApiShop options example
```python
options = {
                'base_url':'/api/',
                'bad_request': True,
                'document': BASE_DIR + '/api_shop/static/document.html', 
                'lang':'en',
                'lang_pack':{}
            }
```
#### ApiShop options description
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
auto_create_folder | bool | False | Automatically create folder. The debug parameter must also be True to take effect.
auto_create_file | bool | False | Automatically create files. The debug parameter must also be True to take effect.
auto_create_class | bool | False | Automatically create class. The debug parameter must also be True to take effect.
auto_create_method | bool | False | Automatically create method. The debug parameter must also be True to take effect.
framework | str | None | Manually specify the framework, currently supports django, flask, bottle, if not specified, the framework will be identified in order, if multiple frames are installed at the same time, please specify manually.
debug | bool | True | An error was thrown when loading the api business code.



### ApiShop options lang_pack description
#### ApiShop options lang_pack example
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


## Api Class component
::: tip
The api business code parent class, the business code you write must inherit it.
:::

### example
``` python
from api_shop import Api

class api_login(Api):
     """User account login, the text here will be loaded into the document """
     def get(self, request, data):
         '''This is the get method of the request'''
         Return

     def post(self, request, data):
         """
         This is the post method of the request
         Data.username # username
         Data.ddd # Date
         """
         Return {'msg': 'Login successful'}

     def patch(self, request, data):
         '''This is the patch method of the request'''
         Return
    
     def delete(self, request, data):
         '''This is the delete method of the request'''
         Return
    
     def put(self, request, data):
         '''This is the put method of the request'''
         Return
```

::: warning return value 
- The return value can be None, and the front end will receive a 200-state empty response, such as return None
- You can also specify a status code, such as return {'msg': 'error message'}, 400
- Of course, you can also return other data directly. return 1 The front end will receive a response with a body content of 1.

:::

### parameter request description
> - Under normal circumstances, the incoming request is the reqeust of the current request.
> - If you use the `get_api_result_json` or `get_api_result_response` method to call the business interface code, if the current request is not passed, the function will forge a fake request, only contains a method attribute, so in the business code, we do not recommend using the request directly. To deal with the problem.

### parameter data description
> - The data object is the check parameter dict, which can access the data content through the attribute, for example: data.name



## Method components
### get_api_result_json method
::: tip
- Call the business code class directly to get the return data and status code
- Please note: All parameters must be filled in the data due to parameter monitoring bypassed.
:::
#### flask example
``` python
from api_shop import get_api_result_json

from views import api_login # Inherited the business code of the Api class

@simple_page.route('/test')
def hello_world(url):
    
    data = get_api_result_json(
        api_login, 'POST', {'name':'testuser','password':'12345'}
        )
    print(data) # This way, the business code can be quickly called inside the program.

```
::: tip get_api_result_json parameter description
- get_api_result_json(api_class, method, data=None, request=None, not200=True)
- Call the api code directly and get the return json
    -    api_class Is the object of the business api class (not an instance)
    -    method Is the request method, str format
    -    data Is additional data, dict format
    -    request=None Is the current request, if the method and request.method are not the same, please encapsulate a request for business code, if the business code does not need reqeust, please do not pass.
    -    not200=True Is to allow the status_code is not equal to 200 results, when it is False, it encounters a program interrupt other than 200 and throws a mistake.
- return json,status_code
:::


### get_api_result_response method
::: tip
- Call the business code class directly, get the response packet response
- Please note: All parameters must be filled in the data due to parameter monitoring bypassed.
:::
#### flask example
``` python
from api_shop import get_api_result_response

from views import api_login 

@simple_page.route('/test')
def hello_world(url):
    
    response = get_api_result_response(
        api_login, 'POST', {'name':'testuser','password':'12345'}
        )
    print(response) 

```
::: tip
Same as the `get_api_result_json` method, but the return value of `get_api_result_response` is a response
:::

## func.model extended functions

### func.model.loads write dict data to ORM stencil
::: tip

The loads method accepts two parameters:

     @model_obj ORM mold object instance

     @dict_data The dict data that needs to be updated

:::
### func.model.dumps Convert the data of ORM mold to json format
::: tip
The dumps method receives the following parameters:

     @model_obj data stencil
     @exclude does not process fields in the list
         Default exclude = ['_sa_instance_state', 'password_hash', '_state', 'password']
         Output password fields are not processed by default
     @include outputs only the fields in the list
     @string directly converted to string format
     @func default output attribute method in stencil class
    
:::
### loads and dumps usage example
```python
from api_shop import func,Api
from models import Users
class users(Api):
    def get(self, request, data):
        user = Users.query.filter(Users.id == data.id).first()
        ret = func.models.dumps(user) # Convert ORM data to json format for front-end use.
        print(ret)
        return {'user':ret}
    def post(self, request, data):
        user = Users.query.filter(Users.id == data.id).first()

        func.models.loads(user, data) # Append the data contained in data to the user

        user.save()
```

### func.model.models_to_list convert the query ORM instance list into a json list
::: tip
Equivalent to [func.model.dumps (x) for x in models]
:::

## data_format Expansion
::: tip Data format extension
- data_format.datetime Can be used to fill in the type in the conf.methods parameter list, convert the string `"2019-01-01 08:30:00"` in the request parameter to datetime format
- data_format.DataExpansion Custom extension base class
:::

### data_format.datetime
``` python
from api_shop import data_format
conf = [
    {
        'url': 'test',
        'class': 'account.views.api_test',
        'name': '测试方法',
        'methods': {
            'POST': [
                {'name':'time', 'type': data_format.datetime, 'required': True, 'min': '2018-01-01', 'max': '2019-12-31', 'description': '时间'}
            ],
        }
    },
]
```
#### When submitting the request, the incoming time parameter will be converted to datetime format, and check whether it is greater than or equal to January 1, 2018, less than or equal to December 31, 2019.

### data_format.regex regular format check
The uploaded string will be checked regularly.
Call method:
```python
from src.api_shop import data_format

conf = [
    {
        'url':'test',
        'class':'business_code.views.api_test',
        'name':'Test interface',
        'methods': {
            'POST': [
                {'name':'email',
                    'type': data_format.regex(
                        r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[ a-zA-Z0-9_-]+){0,4}$',name='mailbox'),
                    'required': True,
                    'min': 6,
                    'max': 24,
                    'description':'Mailbox'
                },
                {'name':'idcard','type': data_format.idcard,'required': True,'description':'ID card'},
            ]
        }
    },
]
```

### Built-in more fast regular check
-data_format.numeric numeric string
-email
-data_format.chinese in Chinese
-data_format.url url format
-data_format.cellphone mobile number
-data_format.idcard ID number




### data_format.DataExpansion custom data type
``` python
from api_shop.data_format import DataExpansion
from datetime import datetime as dt

class datetime(object,metaclass=DataExpansion):
    '''Convert str to datetime format'''
    
    class_name = "<class'data_format.datetime'>"

    def __new__(self, string):
        if':' in string:
            return dt.strptime(string,'%Y-%m-%d %H:%M:%S')
        else:
            return dt.strptime(string,'%Y-%m-%d')
```
::: tip
When inheriting, please follow the above writing, inherit as a metaclass, and directly use the __new__ method to return a new format
:::
