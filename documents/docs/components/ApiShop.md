---
title: ApiShop类
---
## 初始化

::: tip
api-shop核心类，实例化后生成接口对象，你只需要访问实例的方法，就可以调用相应的业务代码。
:::

```python
ap = ApiShop(conf,options)
```

### ApiShop接口配置(conf)

| 键      | 类型          | 说明                                                                                                                                 | 例子                                                   |
| ------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------ |
| url     | str/list      | 接口访问的url，支持list包裹多个url，也支持<参数名>模式，url中添加<参数名>的话，方法参数列表中必须要包含该参数，并指定`required=True` | `login`,`user/<id>`                                    |
| class   | str/Class对象 | 为字符串时，是`Api接口继承对象`的路径，为对象时就是该`Api接口继承对象`                                                               | account.views.api_login                                |
| methods | dict          | 这个对象包含了每个接口可以接受的方法和参数                                                                                           | key可以为GET/POST/PUT/PATCH/PUT/DELETE等http支持的方法 |

#### methods配置说明
::: tip 在配置参数中或者@add_api类装饰器添加
单个methods的value为一个list对象，其中描述了该方法支持的参数
:::
| 键          | 类型                       | 说明                                                                                                                                     | 例子                                                 |
| ----------- | -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| name        | str                        | 参数名字                                                                                                                                 | username                                             |
| type        | object                     | 参数类型，目前支持int，float，list，dict，set，tuple，bool，也支持自定义类型和其他可以被转换的类型                                       | 详情可以查看data_format扩展                          |
| required    | bool                       | 是否必要参数，如果为True，用户请求中没有该参数将会被拦截                                                                                 | 缺省为`False`                                        |
| min         | int                        | 参数的最小值(int)或者最小长度(str/list/set/tuple)，用户提交小于或者短于这个值的参数，将会被拦截                                          | 5                                                    |
| max         | int                        | 参数的最大值(int)或者最大长度(str/list/set/tuple)，用户提交大于或者超过长度的参数，将会被拦截                                            | 5                                                    |
| default     | `同类型参数`、`方法`、`类` | 比如type=int的一个参数，default=1的时候，用户如果不提交参数，将会自动填充1，如果default为一个方法或者类，将会自动填充`运行`/`实例化`结果 |                                                      |
| options     | list                       | 这是参数的可选项，用户提交的参数必须在可选项中，否则将会被拦截                                                                           | options=['a','c'] 表示用户只能提交该参数的值为a或者c |
| description | str                        | 参数的描述，用来给前端开发人员的参考说明                                                                                                 |                                                      |


### ApiShop设置参数(options)

| 参数名称                 | 类型 | 默认值        | 说明                                                                                                                  |
| ------------------------ | ---- | ------------- | --------------------------------------------------------------------------------------------------------------------- |
| base_url                 | str  | /api/         | 基础url，用以组合给前端的api url                                                                                      |
| bad_request              | bool | True          | 参数bad_request如果是真，发生错误返回一个坏请求给前端，否则都返回200的response，里面附带status=error和msg附带错误信息 |
| bad_request_error_status | str  | 'error'       | 默认的bad_request状态信息，bad_request=False生效                                                                      |
| document                 | str  | document.html | 文档模板绝对路径                                                                                                      |
| lang                     | str  | en            | ApiShop的语言，默认为en英文，可选项为zh中文                                                                           |
| debug                    | bool | True          | 是否开启调试信息                                                                                                      |
| auto_create_folder       | bool | False         | 自动创建文件夹（实验方法）                                                                                            |
| auto_create_file         | bool | False         | 自动创建文件（实验方法）                                                                                              |
| auto_create_class        | bool | False         | 自动创建类（实验方法）                                                                                                |
| auto_create_method       | bool | False         | 自动创建方法（实验方法）                                                                                              |





## 业务代码入口
::: tip 实例方法api_entry
实例化ApiShop类之后，需要在web框架的路由中添加一个正则路由，好让api开头的路由，全部被ApiShop接管。
:::

```python
ap = ApiShop(conf,options)

app_name='api'

urlpatterns = [
    path('api_data', ap.get_api_data, name='api_data'), # api文档需要的接口
    path('document/', ap.render_documents, name='document'), #api文档渲染的路由
    re_path(r'([\s\S]*)', ap.api_entry, name='index') # 接管api/下面其他的全部路由到api_entry入口方法
]
```

## 调用其他接口
::: tip 实例方法api_run
从1.12.0版本开始，ApiShop核心类提供了一个api_run的方法，用来在代码中运行另外一个api代码，方便复用。
这个方法将取代原本的get_api_result_json和get_api_result_response
:::
```python
'''
    request   直接传入当前request，
    url       就是你想要访问的接口url
    method    如果不传入，就是 = request.method
    parameter 请求参数，如果不传入，就没有参数传入到api中
    json      默认True返回json数据，False就会返回response
''' 
response_json,code = ap.api_run(request, url, method=None, parameter={'a':1}, json=True)
```

## 执行前钩子
before_running

## 执行后钩子
after_running
## 路由装饰器