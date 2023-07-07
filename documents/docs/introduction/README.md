---
prev:
    text: 首页
    link: /
next:
    text: 快速上手
    link: /start/
lastUpdated: true
---

## 介绍

api-shop 是一个 python 库，它用来帮助使用 django、flask 或者 bottle 作为 web 框架的开发者，快速的进行 restful-api 开发。

### 它是如何工作的？

api-shop 并不会直接接管 web 框架的路由控制器，它需要你在 web 框架的路由控制器中添加一个正则路由，并指向 api-shop 实例入口

比如，在`Flask`中，我们需要你这样引入

```python
from api_shop from ApiShop

af = ApiShop(
    conf=[],
    options={
        'lang': 'zh',
        'framework': 'flask',
    })


@app.route('/api/<regex("([\s\S]*)"):url>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def hello_world(url):
    if url == 'document/':
        return af.render_documents(request, url)
    if url == 'api_data':
        return af.get_api_data(request, url)

    return af.api_entry(request, url)
```

::: tip
其中，`document/`这个路由是可以修改的，`api_data`这个路由确是需要固定的，它是为了默认的文档工具能够拿到接口数据。除非你自己重写文档页面。
:::

## 生命周期

::: tip
让你更加的专注到业务上，其他的事情交给 api-shop
:::
![An image](/api-shop.png)

### 钩子的使用

::: tip
我们提供了 before_running 和 after_running 两个钩子，你只需要继承 ApiShop 并复写它们就可以使用
钩子函数可以返回一个 response 来替代原本将要返回的对象。
:::

### 钩子例子

```python
class CommonApi(ApiShop):
    def before_running(self, **kwargs):
        print('运行前钩子',kwargs)
        if kwargs.get('key')=='addroute/mock':
            return JsonResponse({'msg':'您没有权限'}, status=400)
    def after_running(self, **kwargs):
        print('运行后钩子',kwargs)

af = CommonApi(conf, {
    'framework': 'django',
    'lang': 'zh'
})
```

### before_running 运行前

| 参数名  | 类型                            | 说明                                                              |
| ------- | ------------------------------- | ----------------------------------------------------------------- |
| request | 请求实例                        | 用户提交的请求实例                                                |
| data    | 请求参数对象(该对象继承于 dict) | ApiShop 把请求参数解析后的数据对象，支持 data.name 的方法访问参数 |
| model   | 继承于 Api 类的业务对象         | 接口将要调用的 Api 类                                             |
| key     | str                             | 用户当前引用到的 url 参数（在 conf 配置中的 url 参数）            |

### after_running 运行后

| 参数名   | 类型                    | 说明                                                   |
| -------- | ----------------------- | ------------------------------------------------------ |
| request  | 请求实例                | 用户提交的请求实例                                     |
| response | response 对象           | Api 业务代码执行后，即将返回给用户的 response 对象     |
| model    | 继承于 Api 类的业务对象 | 接口调用的 Api 类                                      |
| key      | str                     | 用户当前引用到的 url 参数（在 conf 配置中的 url 参数） |

## api 网关封装

::: tip
1.14 版本之后提供了一个`SingleApiShop`的全局单例类，用户继承它之后，覆盖`before_running`和`after_running`用来统一处理接口前后内容。
:::
