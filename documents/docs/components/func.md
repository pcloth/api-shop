---
title: 功能扩展
---
## func.model模具相关

### 将dict数据写到ORM模具
::: tip func.model.loads 
loads方法接受两个参数：
1. model_obj   ORM模具对象实例
2. dict_data   需要更新的dict数据
:::
```python
func.model.loads(user,{'nickname':'新昵称','email':'aa@gmail.com'})
```
上面这句代码等同于下面这一段
```python
user.nickname = '新昵称'
user.email = 'aa@gmail.com'
```
这个用来给post更新方法，非常的便捷。

### 将ORM实例数据转换成json
::: tip func.model.dumps
dumps 方法接收参数如下：
1. model_obj 数据模具
2. exclude 不处理列表中的字段
    > 默认值 exclude = ['_sa_instance_state', 'password_hash', '_state', 'password'] 
    > 默认不处理输出密码字段
3. include 只输出列表中的字段
4. string 直接转换成string格式
5. func 默认输出模具类中的属性方法
:::

### 将ORM实例列表转换成json列表
::: tip func.model.models_to_list
等同于[func.model.dumps(x) for x in models]
:::


### loads和dumps使用例子
```python
from api_shop import func,Api
from models import Users
class users(Api):
    def get(self, request, data):
        user = Users.query.filter(Users.id == data.id).first()
        ret = func.models.dumps(user) # 将ORM的数据转换成json格式，方便前端使用。
        print(ret)
        return {'user':ret}
    def post(self, request, data):
        user = Users.query.filter(Users.id == data.id).first()

        func.models.loads(user, data) # 将data包含的数据附加到user上

        user.save()

```

