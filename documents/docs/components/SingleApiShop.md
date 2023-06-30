---
title: SingleApiShop类
---

## 初始化

::: tip
继承自 ApiShop 类，和它的功能一样，唯一区别就是 SingleApiShop 是一个全局单例类，不但保持单例，多次继承也可以保持最后一次单例

`推荐只需要单例的项目中使用SingleApiShop代替ApiShop初始化`
:::

```python
from api_shop import SingleApiShop

class GeteWayApi(SingleApiShop):
    def before_running(self, **kwargs):
        print('运行前钩子',kwargs)
    def after_running(self, **kwargs):
        print('运行后钩子',kwargs)

ap = GeteWayApi(conf,options)
```

## 在其他地方引入

```
from api_shop import SingleApiShop

# 可以获得的GeteWayApi的实例ap，方便在其他代码中调用api接口
api_instance = SingleApiShop.get_single_apishop()

```
