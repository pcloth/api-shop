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
api-shop是一个python库，它用来帮助使用django、flask或者bottle作为web框架的开发者，快速的进行restful-api开发。

### 它是如何工作的？ 
api-shop并不会直接接管web框架的路由控制器，它需要你在web框架的路由控制器中添加一个正则路由，并指向api-shop实例入口

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
让你更加的专注到业务上，其他的事情交给api-shop
:::
![An image](/api-shop.png)

### 钩子的使用
::: tip
我们提供了before_running和after_running两个钩子，你只需要继承ApiShop并复写它们就可以使用
钩子函数可以返回一个response来替代原本将要返回的对象。
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
|参数名|类型|说明|
|---|---|---|
|request|请求实例|用户提交的请求实例|
|data|请求参数对象(该对象继承于dict)|ApiShop把请求参数解析后的数据对象，支持data.name的方法访问参数|
|model|继承于Api类的业务对象|接口将要调用的Api类|
|key|str|用户当前引用到的url参数（在conf配置中的url参数）|


### after_running 运行后
|参数名|类型|说明|
|---|---|---|
|request|请求实例|用户提交的请求实例|
|response|response对象|Api业务代码执行后，即将返回给用户的response对象|
|model|继承于Api类的业务对象|接口调用的Api类|
|key|str|用户当前引用到的url参数（在conf配置中的url参数）|

