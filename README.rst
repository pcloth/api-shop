api-shop

English Documents

https://github.com/pcloth/api-shop/blob/master/README.EN.MD

======================================

    什么是api-shop：提供易用的、轻量化的restful-api接口工具包，基于django或者flask框架。

**demo 图片**
-------------

.. figure:: /static/demo.png
   :alt: demo

   demo
**核心功能：**
--------------

1. 配置化api生成。
2. 自动校验request提交的数据，并转换成制定格式。
3. 自动生成api文档，并提供一个web页面可供查询和mock数据演示。
4. 兼容django 和 flask
5. 容器格式转换，data\_format.datetime格式转换类；'2019-01-18 23:25:25'
   to datetime
6. 自定义格式转换器
7. 多国语言支持。

**更新记录：**
--------------

    2019-01-23

    ver 1.6.0

-  添加多国语言支持，可以在options里指定语言或者扩展语言包。
-  文档改进

**用法：**
----------

1. 安装：

   .. code:: sh

       sudo pip install api-shop

2. 引入：

   .. code:: python

       from api_shop from ApiShop,Api,data_format

+------------+---------------+------------------------------+
| 模块名字   | 功能说明      | 模块介绍                     |
+============+===============+==============================+
| ApiShop    | api初始化类   | 用以加载conf和options        |
+------------+---------------+------------------------------+
| Api        | 业务继承类    | 用来继承后写实际的业务代码   |
+------------+---------------+------------------------------+

3. 初始化 \`\`\` python conf = [ { 'url': 'login', 'class':
   'account.views.api\_login', 'name': '账户登录', 'methods': { 'POST':
   [ {'name':'username', 'type': str, 'required': True, 'min': 3, 'max':
   24, 'description': '用户名'}, {'name':'password', 'type': str,
   'required': True, 'min': 3, 'max': 24, 'description': '密码'}, ],
   'GET':` <#section>`__ } }, ]

\`\`\` > conf 配置说明 > 键 \| 值类型 \| 说明 :----------- \|
:----------- \| -----------: url \| str \|
接口的url地址，只需要填写相对地址 class \| str,class \|
接口实际调用的业务类（继承至Api），可以是对象，也可以是引用地址 name \|
str \| 接口的名字 methods \| dict \| 接口所能接收的methods：有GET POST
DELETE PUT PATCH

    methods 配置说明

    +---------------+-----------+-------------------------------------------------------------------------------------------------------------+
    | 键            | 值类型    | 说明                                                                                                        |
    +===============+===========+=============================================================================================================+
    | name          | str       | 参数名，接收后在data.name                                                                                   |
    +---------------+-----------+-------------------------------------------------------------------------------------------------------------+
    | type          | class     | str,int,float,bool,list,dict,tuple等等，也支持data\_format.datetime时间格式，你也可以自定义一个类型转换器   |
    +---------------+-----------+-------------------------------------------------------------------------------------------------------------+
    | required      | bool      | 是否是必要值                                                                                                |
    +---------------+-----------+-------------------------------------------------------------------------------------------------------------+
    | default       | str       | 当没有接收到时的默认值，注意，它也会被type所指定的类型转换器转换。                                          |
    +---------------+-----------+-------------------------------------------------------------------------------------------------------------+
    | min           | int,str   | 最小值/最小长度，为字符串时，会被type指定的类型转换器转换。                                                 |
    +---------------+-----------+-------------------------------------------------------------------------------------------------------------+
    | max           | int,str   | 最大值/最大长度，为字符串时，会被type指定的类型转换器转换。                                                 |
    +---------------+-----------+-------------------------------------------------------------------------------------------------------------+
    | description   | str       | 功能描述，给前端人员看文档的内容                                                                            |
    +---------------+-----------+-------------------------------------------------------------------------------------------------------------+

4. 配置

   .. code:: python

       options = {
                       'base_url':'/api/',
                       'bad_request': True,
                       'document': BASE_DIR + '/api_shop/static/document.html', 
                       'lang':'en',
                       'lang_pack':{}
                   }

       options 配置说明

       +----------------+-------------+----------+---------------------------------------------------------------+
       | 键             | 值类型      | 默认值   | 说明                                                          |
       +================+=============+==========+===============================================================+
       | base\_url      | str         | /api/    | 接口url前缀                                                   |
       +----------------+-------------+----------+---------------------------------------------------------------+
       | bad\_request   | bool        | True     | 如果请求不合法，是否以坏请求方式返回；否则就是全部是200返回   |
       +----------------+-------------+----------+---------------------------------------------------------------+
       | document       | str(path)   | 略       | 文档页面的html模板所在的路径，默认会有一个简易模板            |
       +----------------+-------------+----------+---------------------------------------------------------------+
       | lang           | str         | en       | 多国语言支持，目前内置en, zh                                  |
       +----------------+-------------+----------+---------------------------------------------------------------+
       | lang\_pack     | dict        | 无       | 扩展语言包，如果你想让api-shop支持更多语言                    |
       +----------------+-------------+----------+---------------------------------------------------------------+

    lang\_pack 语言包

    value 就是目标语言

.. code:: python

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

1. 自定义格式转换器

   .. code:: python

       # 使用自定义格式转换器的时候，min和max也会自动加载这个转换器转换了进行比较
       from datetime import datetime as dt
       class datetime():
           '''将str转换成datetime格式'''
           def __new__(self, string):
               if ':' in string:
                   return dt.strptime(string, '%Y-%m-%d %H:%M:%S')
               else:
                   return dt.strptime(string, '%Y-%m-%d')

例子
----

1. `Django例子 <https://github.com/pcloth/api-shop/tree/master/django_demo>`__
   \`\`\`python ## urls.py from api\_shop import ApiShop

接口配置数据
------------

conf = [ { 'url': 'login', 'class': 'account.views.api\_login',
#需要引入的api类，继承于上面说的Api接口类 'name': '账户登录', 'methods':
{ 'POST': [ {'name':'username', 'type': str, 'required': True, 'min': 3,
'max': 24, 'description': '用户名'}, {'name':'password', 'type': str,
'required': True, 'min': 3, 'max': 24, 'description': '密码'}, ] ##
这里可以插入更多的methods，比如GET,DELETE,POST,PATCH } }, ##
这里可以插入更多的api接口

]

api-shop参数设置：
------------------

options = { 'base\_url':'/api/',# 基础url，用以组合给前端的api url
可默认 # 'document':BASE\_DIR+'/api\_shop/static/document.html', #
文档路由渲染的模板 可默认 'bad\_request':True, #
参数bad\_request如果是真，发生错误返回一个坏请求给前端，否则都返回200的response，里面附带status=error和msg附带错误信息
可默认 }

ap = ApiShop(conf,options)

app\_name='api'

urlpatterns = [ path('api\_data', ap.get\_api\_data, name='api\_data'),
# api文档需要的接口 path('document/', ap.render\_documents,
name='document'), #api文档渲染的路由 re\_path(r'([]\*)', ap.api\_entry,
name='index') # 接管api/下面其他的全部路由到api\_entry入口方法 ]

\`\`\`

.. code:: python

    ## account/views.py
    from api_shop from Api

    class api_login(Api):
        def post(self,request,data=None):
            '''api登陆接口，方便微信用户绑定账户'''
            username = data.username
            password = data.password
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                token = TokenBackend.make_token(user).decode('utf-8')
                return JsonResponse({'status': 'success', 'msg': '执行成功', 'token': token})
            
            return JsonResponse({'status': 'error', 'msg': '用户登录失败'})

2. `flask例子 <https://github.com/pcloth/api-shop/tree/master/flask_demo>`__
   \`\`\`python from flask import Flask,request,render\_template\_string

from werkzeug.routing import BaseConverter

from api\_shop import ApiShop,Api

class RegexConverter(BaseConverter): def **init**\ (self, map, \*args):
self.map = map self.regex = args[0]

app = Flask(\ **name**) #
如果使用蓝图，添加正则处理器必须是在注册蓝图之前使用。
app.url\_map.converters['regex'] = RegexConverter

conf = [ { 'url': 'login', 'class': 'api.views.api\_login', 'name':
'账户登录', 'methods': { 'POST': [ {'name':'username', 'type': str,
'required': True, 'min': 3, 'max': 24, 'description': '用户名'},
{'name':'password', 'type': str, 'required': True, 'min': 3, 'max': 24,
'description': '密码'}, ] } }, { 'url': 'test', 'class':
'api.views.test', 'name': '测试数据', 'methods': { 'GET':[{'name':'bb',
'type': int, 'required': True, 'min': 0, 'max': 100, 'description':
'百分比','default':95},], 'POST': [ {'name':'add', 'type': str,
'required': True, 'min': 3, 'max': 24, 'description': '地址'},
{'name':'bb', 'type': int, 'required': True, 'min': 0, 'max': 100,
'description': '百分比','default':95}, {'name':'list', 'type': list,
'description': '列表'}, ], 'DELETE':[ {'name':'id', 'type': int,
'required': True, 'min': 1,'description': '编号'}, ] } },

]

af = ApiShop(conf)

@app.route('/api/',methods=['GET', 'POST','PUT','DELETE','PATCH']) def
hello\_world(url): print(url) if url=='document/': return
af.render\_documents(request,url) if url=='api\_data': return
af.get\_api\_data(request,url)

::

    return af.api_entry(request,url)

if **name** == '**main**\ ': app.run(host="0.0.0.0",debug=True) \`\`\`
