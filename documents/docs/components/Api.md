---
title: Api类
---

## Api类
::: tip
api业务代码父类，你写的业务代码都要继承它。
:::

## 例子
``` python
from api_shop import Api, ApiResponseModelFields

class api_login(Api):
    """用户账号登陆，这里的文字会被加载到文档里"""
    response_docs = {
        # 这个response_docs将会在文档中生成返回值说明文档
        'get':{
            'results':{PartyData},
            'test':{
                ApiResponseModelFields(PartyData,['id',PartyData.name]), # 使用部分字段，django必须使用这个类包裹才能引入部分字段，flask则可以直接使用字段名
                'photos:Array:照片数据' # 手写字段文档
                },
            'user_party_info':{PartyUsers,'photos:Array:照片数据'} # PartyUsers模型的全部字段叠加部分其他字段
        }
    }

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

## methods类方法
::: tip 
1. get 方法，对应的是request的`get` method
2. post 方法，对应的是request的`post` method
3. patch 方法，对应的是request的`patch` method
4. delete 方法，对应的是request的`delete` method
5. put 方法，对应的是request的`put` method
:::

### 传入的 request 说明
> - 正常情况下，传入的request就是当前请求的reqeust

### 传入的 data 说明
> - data对象就是校验转换后的参数dict，数据内容可以通过属性访问，例如：data.name


## response_docs返回值文档
这个response_docs将会在文档中生成返回值说明文档
> 它的第一层是一个dict字典，key为method名。
> 第二层开始就是描述返回值的说明，可以直接使用orm的model类对象。
> 也可以使用ApiResponseModelFields类方法来包裹ORM的Model类，并描述需要的部分字段
> 甚至你可以使用用冒号分割的一个字符串描述`'photos:Array:照片数据'` # 手写字段文档

## ApiResponseModelFields
这个类可以捕捉ORM的数据模型里面的字段和描述信息，用来生成返回值文档
```py
ApiResponseModelFields(Model,List)
```
::: tip 
ApiResponseModelFields初始化需要两个参数。
Model为你需要引用的ORM数据模型
List是包含了需要返回字段的列表，列表中可以是字符串key，也可以是Model.key （key为字段名）
:::

### response_docs在文档中的表现
![response_docs](/responseDocs.png)
