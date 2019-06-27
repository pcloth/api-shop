# 组件

模块名字 | 功能说明 | 模块介绍
:----------- | :-----------: | :-----------
ApiShop         | api初始化类        | 用以加载conf和options
Api         | 业务基础类        | 用来继承后写实际的业务代码

get_api_result_json         | 直接调用业务类        | 返回 json,status_code
get_api_result_response         | 直接调用业务类        | 返回response
data_format | 内置自定义数据格式 | data_format.datetime 可以将一个字符串转换成datetime格式
data_format.DataExpansion | 自定义数据基础类 | 用来写自定义数据格式



## ApiShop 类组件
::: tip
api-shop核心类，实例化后生成接口对象，你只需要访问实例的方法，就可以调用相应的业务代码。
:::


```python
ap = ApiShop(conf,options)
```

### ApiShop conf 说明
#### ApiShop conf 例子
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

#### ApiShop conf 详细
键 | 值类型 | 说明
:----------- | :----------- | -----------:
url         | str,list        | 接口的url地址，只需要填写相对地址，如果有多条url，可以配置成`list`。支持url参数：`/api/url/<id>`
class         | str,class        | 接口实际调用的业务类（继承至Api），可以是对象，也可以是引用地址
name         | str        | 接口的名字
methods         | dict        | 接口所能接收的methods：有GET POST DELETE PUT PATCH

### ApiShop conf methods 说明
#### ApiShop conf methods 详细
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


### ApiShop options 说明
#### ApiShop options 例子
```python
options = {
                'base_url':'/api/',
                'bad_request': True,
                'document': BASE_DIR + '/api_shop/static/document.html', 
                'lang':'en',
                'lang_pack':{}
            }
```
#### ApiShop options 详细
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
auto_create_folder | bool | False | 自动创建文件夹，debug参数也必须为True才可以生效。
auto_create_file | bool | False | 自动创建文件，debug参数也必须为True才可以生效。
auto_create_class | bool | False | 自动创建类，debug参数也必须为True才可以生效。
auto_create_method | bool | False | 自动创建方法，debug参数也必须为True才可以生效。
framework | str | 无 | 手动指定框架，目前支持django、flask、bottle，如果不指定，将按顺序识别框架，如果同时安装了多个框架，请手动指定。
debug | bool | True | 加载api业务代码的时候，遇到错误抛出。

### ApiShop options lang_pack 说明
#### ApiShop options lang_pack 例子
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


## Api 类组件
::: tip
api业务代码父类，你写的业务代码都要继承它。
:::

### 例子
``` python
from api_shop import Api

class api_login(Api):
    """用户账号登陆，这里的文字会被加载到文档里"""
    def get(self, request, data):
        '''这是request的get方法'''
        return 

    def post(self, request, data):
        """ 
        这是request的post方法
        data.username # 用户名
        data.ddd # 日期
        """
        return {'msg':'登陆成功'}

    def patch(self, request, data):
        '''这是request的patch方法'''
        return 
    
    def delete(self, request, data):
        '''这是request的delete方法'''
        return 
    
    def put(self, request, data):
        '''这是request的put方法'''
        return 
```

::: warning 返回值 
- 返回值可以为None，前端会收到一个200状态的空响应，例如 return None
- 也可以指定状态码，比如 return {'msg':'错误信息'}, 400
- 当然也可以直接返回其他数据 return 1  前端会收到一个body内容为1的响应

:::

### 传入的 request 说明
> - 正常情况下，传入的request就是当前请求的reqeust
> - 如果使用`get_api_result_json`或`get_api_result_response`方法调用业务接口代码的时候，如果没有传入当前request，函数会伪造一个虚假的request，只包含一个method属性，所以在业务代码中，我们不推荐直接使用request来处理问题。

### 传入的 data 说明
> - data对象就是校验转换后的参数dict，数据内容可以通过属性访问，例如：data.name



## 方法组件
### get_api_result_json 方法
::: tip
- 直接调用业务代码类，获取返回数据和状态码
- 请注意：由于绕开了参数监测，所有参数都必须填写在data中，没有的用None填写
:::
#### flask 例子
``` python
from api_shop import get_api_result_json

from views import api_login # 继承了Api类的业务代码

@simple_page.route('/test')
def hello_world(url):
    
    data = get_api_result_json(
        api_login, 'POST', {'name':'testuser','password':'12345'}
        )
    print(data) # 这样在程序内部也能快速的调用业务代码。

```
::: tip get_api_result_json 参数说明
- get_api_result_json(api_class, method, data=None, request=None, not200=True)
- 直接调用api代码，并拿到返回json
    -    api_class 是业务api类的对象（不是实例）
    -    method 是请求方法,str格式
    -    data 是附加数据，dict格式
    -    request=None 是当前request,如果method和request.method不相同，请自己封装一个适合业务代码用的request，如果业务代码不用reqeust，请不要传入。
    -    not200=True 是允许status_code不等于200的结果，为False的时候，遇到200以外程序中断并抛错
- return json,status_code
:::


### get_api_result_response 方法
::: tip
- 直接调用业务代码类，获取返回响应包response
- 请注意：由于绕开了参数监测，所有参数都必须填写在data中，没有的用None填写
:::
#### flask 例子
``` python
from api_shop import get_api_result_response

from views import api_login # 继承了Api类的业务代码

@simple_page.route('/test')
def hello_world(url):
    
    response = get_api_result_response(
        api_login, 'POST', {'name':'testuser','password':'12345'}
        )
    print(response) # 这样在程序内部也能快速的调用业务代码。

```
::: tip
和get_api_result_json方法是一样的，不过get_api_result_response的返回值是一个response
:::


## data_format 扩展
::: tip 数据格式扩展
- data_format.datetime 可以用来填写在conf.methods参数列表中的type，将request参数中的字符串`"2019-01-01 08:30:00"`转换成datetime格式
- data_format.DataExpansion 自定义扩展基础类
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
#### 提交请求的时候，会把传入的time参数转换成datetime格式，并检查是否大于等于2018年1月1日，小于等于2019年12月31日。

### data_format.DataExpansion
``` python
from api_shop.data_format import DataExpansion
from datetime import datetime as dt

class datetime(object,metaclass=DataExpansion):
    '''将str转换成datetime格式'''
    
    class_name = "<class 'data_format.datetime'>"

    def __new__(self, string):
        if ':' in string:
            return dt.strptime(string, '%Y-%m-%d %H:%M:%S')
        else:
            return dt.strptime(string, '%Y-%m-%d')
```

#### 继承的时候请按照上面的写法，继承为元类，并直接用__new__方法来返回一个全新的格式
