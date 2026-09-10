---
title: 框架适配器
---

# 框架适配器

2.0 不再使用 `SingleApiShop` 保存全局实例。每个宿主应用创建自己的 `Dispatcher`，再挂载一个 catch-all adapter。

## ASGI

```python
from api_shop.adapters import ASGIAdapter

application = ASGIAdapter(dispatcher, prefix="/api")
```

ASGI adapter 无额外框架依赖，支持 JSON、URL encoded form 和重复 query 参数。multipart 上传应使用宿主框架 adapter，或在上游 middleware 中解析。

## Flask

```python
from api_shop.adapters import mount_flask

mount_flask(app, dispatcher, prefix="/api", endpoint="api_shop")
```

它会注册 `/api` 和 `/api/<path>` 两个入口。`endpoint` 在同一个 Flask app 中必须唯一。

## Django

```python
from api_shop.adapters import django_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    *django_urlpatterns(dispatcher, prefix="api"),
]
```

如果项目已有更具体的 URL，应把 catch-all 放在它们之后。

## Bottle

```python
from api_shop.adapters import mount_bottle

mount_bottle(app, dispatcher, prefix="/api")
```

## Adapter 的边界

adapter 只负责传输层转换：

- 保留重复 query 值。
- 区分 JSON body、form 和 files。
- 不改变核心错误结构。
- 将 `X-Request-ID` 写回响应。

业务代码只依赖 `RequestContext`，不应依赖某个框架的全局 request。确有需要时可以临时读取 `ctx.raw`，但这会降低跨框架可移植性。
