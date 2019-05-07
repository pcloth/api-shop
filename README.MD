# api-shop

# [English Documents](./README.EN.MD)

> ### api-shop：一个易用的、快速的restful-api接口工具包，兼容：`django` / `flask` / `bottle`。
> ### `一切只为少加班。`

## **demo 图片**

![demo](/static/demo.png)


## **核心功能：**
1. 配置化api生成。
2. 自动校验request提交的数据，并转换成指定格式，支持：int，float，list，dict，set，tuple，bool
3. 自动生成api文档，并提供一个web页面可供查询和mock数据演示。
4. 兼容 `django` , `flask` , `bottle` (如果不指定框架，默认按这个顺序识别框架)
5. 自动生成接口`骨架文件`功能（请谨慎开启）。
6. 自定义格式转换器，data_format.datetime格式转换类；'2019-01-18 23:25:25' to datetime
7. 多国语言支持，也支持自定义语言包。
8. 文档热重载。
9. 默认值支持方法函数。
10. 支持url中包含参数，例如 `/api/user/<id>`，并且在配置methods参数的时候设置它的规则。
11. 支持多url绑定一个接口
12. 支持指定参数的可选项，例如：[1,4,7]，收到这个列表之外的参数就会触发bad_request
13. 可以在代码中直接调用Api业务代码：`get_api_result_json`和`get_api_result_response`

## **更新记录：**
> 2019-05-07 
>
> var 1.9.0
- 添加代码复用方法：`get_api_result_json`和`get_api_result_response`
- 可以直接调用api的返回值


> 2019-04-03 
>
> var 1.8.0
- 支持指定参数的可选项，例如：[1,4,7]，收到这个列表之外的参数就会触发bad_request


> 2019-04-03 
>
> var 1.7.3
- 添加支持多url绑定一个接口支持。
```python
{
        'url': ['weixin','weixin/<name>/<id>'],
        'class': 'business_code.views.test',
        'name': '账户登录',
        'methods': {
            'POST': [
                {'name': 'id', 'type': bool, 'required': True,'description': '用户id'},
                {'name': 'name', 'type': str, 'min':4,'required': True,'description': '用户name'}, 
            ],
        }
    },
```

> 2019-03-15 
>
> var 1.7.2
- 进一步抽象优化代码，便于添加新框架支持。
- 添加bottle框架支持。
- 添加bad_request_error_status参数，当bad_request==False的时候，bad_request_error_status是返回给坏请求的自定义错误状态信息


> 2019-03-14
>
> ver 1.7.1
- 优化框架加载逻辑，默认加载框架顺序```django``` -> ```flask```；添加配置参数直接指定框架。
- 优化部分正则处理逻辑。


> 2019-03-12
>
> ver 1.7.0
- 添加根据配置文件自动生成接口骨架文件：当你添加conf内容的时候，api-shop会根据其内容自动创建
  目录、文件、引入模块、创建类和方法，以及根据接口配置的参数创建备注信息，减少你的代码量。
- 例如：
```python
af = ApiShop(conf,
    {
        'lang': 'zh',
        'name_classification': ['微信', '账户'],
        'url_classification': ['weixin', 'login'],
        'auto_create_folder': True,  # 自动创建文件夹
        'auto_create_file': True,  # 自动创建文件
        'auto_create_class': True,  # 自动创建类
        'auto_create_method': True,  # 自动创建方法
    })
```

生成后的文件
```python
# api-shop automatically inserts code
from api_shop import Api


class api_login(Api):
    """微信账户登录"""
    pass
    def post(self, request, data):
        """ todo:
        api-shop automatically inserts code
        data.username # 用户名
        data.ddd # 日期
        """
        pass
```


> 2019-03-06
>
> ver 1.6.7
- 添加url参数支持
- 例如：
```python
conf = [{
        'url': 'weixin/<name>/<id>',
        'class': 'business_code.views.test',
        'name': 'test api',
        'methods': {
            
            'POST': [
                {'name': 'id', 'type': int, 'required': True, 'description': '用户id'},
                {'name': 'name', 'type': str, 'min':4,'required': True,'description': '用户name'}, 
            ],
        }
    },]
```



> 2019-02-25
>
> ver 1.6.5
- 添加空Response支持，Api方法可以不返回任何值
- 添加对bool参数类型的支持
- 接口文档支持过滤（需配置options）



## **用法：**
1. 安装：
```sh
sudo pip install api-shop
```

2. 引入：
```python
from api_shop from ApiShop,Api,data_format
```

模块名字 | 功能说明 | 模块介绍
:----------- | :-----------: | :-----------
ApiShop         | api初始化类        | 用以加载conf和options
Api         | 业务继承类        | 用来继承后写实际的业务代码
DataFormat | 自定义数据继承类 | 用来写自定义数据格式
get_api_result_json         | 直接调用业务类        | 返回 json,status_code
get_api_result_response         | 直接调用业务类        | 返回response
data_format | 内置自定义数据格式 | data_format.datetime 可以将一个字符串转换成datetime格式



3. 初始化
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
> conf 配置说明
> 
键 | 值类型 | 说明
:----------- | :----------- | -----------:
url         | str,list        | 接口的url地址，只需要填写相对地址，如果有多条url，可以配置成`list`。支持url参数：`/api/url/<id>`
class         | str,class        | 接口实际调用的业务类（继承至Api），可以是对象，也可以是引用地址
name         | str        | 接口的名字
methods         | dict        | 接口所能接收的methods：有GET POST DELETE PUT PATCH

> methods 配置说明
> 
键 | 值类型 | 说明
:----------- | :----------- | -----------:
name         | str        | 参数名，接收后在data.name
type         | class        | str,int,float,bool,list,dict,tuple等等，也支持data_format.datetime时间格式，你也可以自定义一个类型转换器
required         | bool        | 是否是必要值
default         | str,function        | 当没有接收到时的默认值，注意，它也会被type所指定的类型转换器转换。当它是一个function时，如果没有收到请求参数，将会自动运行这个方法获取值，同时将不再进行类型转换。
min         | int,str        | 最小值/最小长度，为字符串时，会被type指定的类型转换器转换。
max         | int,str        | 最大值/最大长度，为字符串时，会被type指定的类型转换器转换。
description         | str        | 功能描述，给前端人员看文档的内容
options    | list | 参数必须在这个列表中的值，例如：[1,4,7]，收到这个列表之外的参数就会触发bad_request

4. 配置
```python
options = {
                'base_url':'/api/',
                'bad_request': True,
                'document': BASE_DIR + '/api_shop/static/document.html', 
                'lang':'en',
                'lang_pack':{}
            }
```
> options 配置说明
> 
键 | 值类型 | 默认值 | 说明
:----------- | :----------- | :----------- | -----------:
base_url         | str        | /api/ | 接口url前缀
bad_request         | bool        | True | 如果请求不合法，是否以坏请求方式返回；否则就是全部是200返回
bad_request_error_status | str,int,bool | 'error' | 如果bad_request参数设置为False，那么这个参数就会启用，会在坏请求里附带一个status='error'的信息，你可以自定义这个信息。
document         | str(path)        | 略 | 文档页面的html模板所在的路径，默认会有一个简易模板
lang         | str        | en | 多国语言支持，目前内置en, zh
lang_pack         | dict        | 无 | 扩展语言包，如果你想让api-shop支持更多语言
name_classification | list | 无 | 用于默认的文档模板对接口名称进行过滤，便于查找
url_classification | list | 无 | 用于默认的文档模板对接口url进行过滤，便于查找。例子：'url_classification':['weixin','login']
auto_create_folder | bool | False | 自动创建文件夹
auto_create_file | bool | False | 自动创建文件
auto_create_class | bool | False | 自动创建类
auto_create_method | bool | False | 自动创建方法
framework | str | 无 | 手动指定框架，目前支持django、flask、bottle，如果不指定，将按顺序识别框架，如果同时安装了多个框架，请手动指定。



> lang_pack 语言包
> 
> value 就是目标语言
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

1. 自定义格式转换器
```python
# 使用自定义格式转换器的时候，min和max也会自动加载这个转换器转换了进行比较
from datetime import datetime as dt
class datetime():
    '''将str转换成datetime格式'''
    def __new__(self, string):
        if ':' in string:
            return dt.strptime(string, '%Y-%m-%d %H:%M:%S')
        else:
            return dt.strptime(string, '%Y-%m-%d')
```


## 例子

1. [Django例子]
```python
## urls.py
from api_shop import ApiShop

## 接口配置数据
conf = [
    {
        'url': 'login',
        'class': 'account.views.api_login', #需要引入的api类，继承于上面说的Api接口类
        'name': '账户登录',
        'methods': {
            'POST': [
                {'name':'username', 'type': str, 'required': True, 'min': 3, 'max': 24, 'description': '用户名'},
                {'name':'password', 'type': str, 'required': True, 'min': 3, 'max': 24, 'description': '密码'},
            ]
            ## 这里可以插入更多的methods，比如GET,DELETE,POST,PATCH
        }
    },
    ## 这里可以插入更多的api接口

]

## api-shop参数设置：

options = {
            'base_url':'/api/',# 基础url，用以组合给前端的api url 可默认
            # 'document':BASE_DIR+'/api_shop/static/document.html', # 文档路由渲染的模板 可默认
            'bad_request':True, # 参数bad_request如果是真，发生错误返回一个坏请求给前端，否则都返回200的response，里面附带status=error和msg附带错误信息 可默认
        }


ap = ApiShop(conf,options)

app_name='api'

urlpatterns = [
    path('api_data', ap.get_api_data, name='api_data'), # api文档需要的接口
    path('document/', ap.render_documents, name='document'), #api文档渲染的路由
    re_path(r'([\s\S]*)', ap.api_entry, name='index') # 接管api/下面其他的全部路由到api_entry入口方法
]

```

### 
```python
## account/views.py
from api_shop from Api

class api_login(Api):
    def post(self,request,data):
        '''api登陆接口，方便微信用户绑定账户'''
        username = data.username
        password = data.password
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            token = TokenBackend.make_token(user).decode('utf-8')
            return {'status': 'success', 'msg': '执行成功', 'token': token}
        
        return {'status': 'error', 'msg': '用户登录失败'},400 # 400如果省略，会默认200的http code
```




1. [flask例子]
```python
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






