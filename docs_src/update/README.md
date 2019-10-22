# 更新记录

---
> 2019-10-22 
>
> var 1.9.7
- 容错：当前端参数为空字符串时，参数type!=str的时候，自动转换成None；参数type==str的时候，保留空字符串。
---

---
> 2019-09-05 
>
> var 1.9.5
- 优化文档页面，添加全文搜索功能。
---

---
> 2019-09-04 
>
> var 1.9.4
- 重构文档模板页面，添加了前端路由支持，url包含了当前接口信息，方便交流沟通。
---


---
> 2019-06-27 
>
> var 1.9.2
- 添加`debug`参数，默认为True，当它为True的时候，自动填充功能才有可能生效（当然也必须开启相应的参数。）
- 开启后如果加载业务代码失败，会抛出错误并中断程序。
---



---
> 2019-05-07 
>
> var 1.9.0
- 添加代码复用方法：`get_api_result_json`和`get_api_result_response`
- 可以直接调用api的返回值
---

---
> 2019-04-03 
>
> var 1.8.0
- 支持指定参数的可选项，例如：[1,4,7]，收到这个列表之外的参数就会触发bad_request
---

---
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
---

---
> 2019-03-15 
>
> var 1.7.2
- 进一步抽象优化代码，便于添加新框架支持。
- 添加bottle框架支持。
- 添加bad_request_error_status参数，当bad_request==False的时候，bad_request_error_status是返回给坏请求的自定义错误状态信息
---

---
> 2019-03-14
>
> ver 1.7.1
- 优化框架加载逻辑，默认加载框架顺序```django``` -> ```flask```；添加配置参数直接指定框架。
- 优化部分正则处理逻辑。
---

---
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
---


---
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
---

---
> 2019-02-25
>
> ver 1.6.5
- 添加空Response支持，Api方法可以不返回任何值
- 添加对bool参数类型的支持
- 接口文档支持过滤（需配置options）
---
