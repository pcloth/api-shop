---
home: true
heroImage: /logo.png
description: "框架无关、类型驱动的 Python API 契约与调度器。"
actions:
    - text: 快速上手 →
      link: /start/
      type: primary
    - text: 从 1.x 升级
      link: /migration/
features:
    - title: 一份契约
      details: Pydantic 类型模型同时驱动参数绑定、运行时校验、响应过滤和 OpenAPI 3.1。
    - title: 框架无关
      details: 核心只处理 RequestContext 和 ResponseContext，通过一个 catch-all 接入 ASGI、Django、Flask 或 Bottle。
    - title: 安全且可预测
      details: 路由在启动时编译，参数来源显式声明，响应始终按已声明契约校验。
footer: BSD-3-Clause Licensed | api-shop 2.0
---

![PyPI](https://img.shields.io/pypi/v/api-shop?logo=api-shop) ![PyPI - Downloads](https://img.shields.io/pypi/dm/api-shop)

## api-shop 2.0

api-shop 2.0 不再把框架、路由配置和返回值转换保存在全局对象中。每个应用拥有独立的 `ApiRegistry` 和 `Dispatcher`：

```text
宿主框架 catch-all
        ↓
RequestContext
        ↓
路由匹配 → 参数绑定/校验 → 中间件 → Handler
        ↓
响应校验/序列化 → ResponseContext
```

核心能力：

1. 用标准 Python 类型和 Pydantic v2 声明输入、输出。
2. 显式区分 Path、Query、Header、Cookie、Body、Form 和 File。
3. 支持同步与异步 handler、中间件和统一错误结构。
4. 支持 `int`、`uuid`、`slug`、`path` 路由转换器和确定性优先级。
5. 从实际运行契约生成 OpenAPI 3.1。
6. 通过显式字段白名单从 Django ORM、SQLAlchemy 生成 DTO。
7. 保留 1.x 兼容入口，支持渐进迁移。

::: warning 2.0 是大版本升级
`ApiShop`、`Api`、`SingleApiShop` 仍可从 `api_shop.legacy` 使用，但已经弃用。新接口应使用 `ApiRegistry`、`Dispatcher` 和类型化契约。
:::
