---
title: 数据类型扩展
---
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

### data_format.regex 正则格式校验
将对上传的字符串进行正则校验。
调用方法：
```python
from src.api_shop import data_format

conf = [
    {
        'url': 'test',
        'class': 'business_code.views.api_test',
        'name': '测试接口',
        'methods': {
            'POST': [
                {'name': 'email', 
                    'type': data_format.regex(
                        r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$',name='邮箱'), 
                    'required': True, 
                    'min': 6, 
                    'max': 24, 
                    'description': '邮箱'
                },
                {'name':'idcard', 'type': data_format.idcard, 'required': True, 'description': '身份证'},
            ]
        }
    },
]
```

### 内置更多的快速正则校验
- data_format.numeric 数字型字符串
- email 邮箱
- data_format.chinese 中文
- data_format.url url格式
- data_format.cellphone 手机号码
- data_format.idcard 身份证号码




### data_format.DataExpansion 自定义数据类型
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
::: tip
继承的时候请按照上面的写法，继承为元类，并直接用__new__方法来返回一个全新的格式
:::
