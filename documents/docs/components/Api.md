---
title: 请求与响应契约
---

# 请求与响应契约

## 参数来源

输入模型必须继承 `pydantic.BaseModel`，每个字段必须且只能声明一个来源：

```python
from typing import Annotated
from pydantic import BaseModel
from api_shop import Body, Cookie, File, Form, Header, Path, Query


class SearchBody(BaseModel):
    filters: list[str] = []


class SearchInput(BaseModel):
    project_id: Annotated[int, Path()]
    page: Annotated[int, Query()] = 1
    token: Annotated[str, Header(alias="Authorization")]
    session: Annotated[str | None, Cookie(alias="session_id")] = None
    body: Annotated[SearchBody, Body()]
```

| 来源 | 数据位置 | 备注 |
| --- | --- | --- |
| `Path` | 路由变量 | 字段必须与路由变量一一对应 |
| `Query` | URL query | 重复 key 保留为 list |
| `Header` | 请求头 | 名称匹配不区分大小写，可用 alias |
| `Cookie` | Cookie | 可用 alias |
| `Body` | 完整 JSON body | 一个模型最多声明一个，不能与 Form/File 混用 |
| `Form` | 表单字段 | 可与 File 组合 |
| `File` | 上传文件 | 实际对象类型由宿主 adapter 决定 |

参数不会在来源之间自动回退。这样可以避免 query 参数意外覆盖 body，也让 OpenAPI 与运行时行为一致。

## RequestContext

handler 的第一个参数是 `RequestContext`：

```python
ctx.method
ctx.path
ctx.headers
ctx.query
ctx.cookies
ctx.body
ctx.form
ctx.files
ctx.path_params
ctx.state
ctx.request_id
ctx.raw
```

`ctx.raw` 是宿主框架原始请求，仅用于尚未抽象的特殊功能。可复用业务代码应优先使用其他标准字段。

## 响应契约

```python
class UserOutput(BaseModel):
    id: int
    display_name: str


class ErrorOutput(BaseModel):
    reason: str


@api.route(
    "/users/<int:id>",
    methods=["GET"],
    input=GetUserInput,
    response={200: UserOutput, 404: ErrorOutput},
)
def get_user(ctx, data):
    ...
```

响应校验既用于检查契约，也会过滤模型中未声明的字段。不要把 ORM 模型整对象直接作为公共响应契约，应建立明确的输出 DTO。

## 错误结构

路由、方法、请求校验和内部错误使用同一结构：

```json
{
  "error": {
    "code": "validation_error",
    "message": "Request validation failed",
    "details": [
      {
        "location": ["query", "page"],
        "code": "greater_than_equal",
        "message": "Input should be greater than or equal to 1"
      }
    ],
    "request_id": "8bc1..."
  }
}
```

常用状态：

| 场景 | HTTP 状态 | code |
| --- | ---: | --- |
| 路由不存在 | 404 | `route_not_found` |
| Method 不允许 | 405 | `method_not_allowed` |
| 参数校验失败 | 422 | `validation_error` |
| 未处理异常 | 500 | `internal_error` |
| 响应契约失败 | 500 | `response_validation_error` |

业务异常可以抛出 `ApiError(status, code, message, details=...)`。500 级异常不要把内部堆栈或模型数据写进客户端响应。
