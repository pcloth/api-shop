# 核心组件

| 组件 | 职责 |
| --- | --- |
| `ApiRegistry` | 声明并编译路由、输入模型、响应模型和 OpenAPI 元数据 |
| `Dispatcher` | 参数绑定、校验、middleware、handler 调用和响应校验 |
| `RequestContext` | 与框架无关的请求上下文 |
| `ResponseContext` | 与框架无关的响应对象 |
| 来源标记 | `Path`、`Query`、`Header`、`Cookie`、`Body`、`Form`、`File` |
| adapters | ASGI、Django、Flask、Bottle 的 catch-all 接入 |
| `generate_openapi` | 从已编译的运行契约生成 OpenAPI 3.1 |
| ORM inspectors | 显式选择 ORM 字段并生成 Pydantic DTO |
| `api_shop.legacy` | 1.x 临时兼容及 conf 迁移 |

推荐阅读顺序：

1. [ApiRegistry 与 Dispatcher](./ApiShop.md)
2. [请求与响应契约](./Api.md)
3. [框架适配器](./SingleApiShop.md)
4. [OpenAPI 与 ORM](./func.md)
5. [校验与自定义类型](./data_format.md)

::: warning 旧组件
`ApiShop`、`SingleApiShop`、`Api`、`ApiResponseModelFields` 和 `data_format` 属于 1.x 兼容 API。请参阅[升级指南](/migration/)，不要在新接口中继续使用。
:::
