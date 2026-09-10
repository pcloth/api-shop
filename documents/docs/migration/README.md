---
prev:
    text: 快速上手
    link: /start/
next:
    text: 核心组件
    link: /components/
lastUpdated: true
---

# 从 1.x 升级到 2.0

2.0 保留了旧 API，但运行模型已经改变。推荐分接口渐进迁移，不建议一次性机械重写全部业务。

## 升级前必须注意

### 运行环境和依赖

- Python 最低版本提高到 3.10。
- 参数模型依赖 Pydantic 2.x。
- Django、Flask、Bottle、SQLAlchemy 改为可选 extra，不再由核心包全部安装。
- 先在独立分支升级依赖并运行完整接口测试，不要直接覆盖生产环境。

### 行为变化

- 新 API 不再自动识别当前框架，必须显式挂载 adapter。
- 新参数必须标记来源；query 和 JSON body 不再因为 `if/elif` 而互相丢失。
- bool 只接受 `true`、`false`、`1`、`0` 及对应布尔/整数值，`yes` 或任意文本会返回 422。
- 路由 converter 会真正参与匹配和转型，静态路由优先于动态路由。
- 声明响应模型后，未声明的状态码或不符合模型的返回值会转换为 500；详细原因只写日志。
- 错误响应统一为 `error.code/message/details/request_id`，不再支持把参数错误伪装为 HTTP 200。
- runtime 自动创建目录、文件、类和方法已经禁用。
- 不再推荐 `SingleApiShop`、全局 hook、`api_run` 和直接返回框架 Response。

## 推荐迁移路径

### 第一步：原样运行旧接口

旧入口仍然可以使用，但应显式从 legacy 模块导入：

```python
from api_shop.legacy import Api, ApiShop, SingleApiShop
```

这一步只用于争取迁移时间。旧实现仍保留 1.x 的全局状态限制，并会产生弃用警告。

### 第二步：把旧 conf 接到新调度器

无需立即改写 handler，可以先转换配置：

```python
from api_shop.legacy import dispatcher_from_conf
from api_shop.adapters import mount_flask

dispatcher = dispatcher_from_conf(old_conf)
mount_flask(app, dispatcher, prefix="/api")
```

转换器不会修改原始 `conf`。未声明来源的旧参数临时使用：

```text
path > JSON body > form > query
```

如果同名参数存在多个来源，优先级高的值生效。应尽快通过类型化契约消除这种隐式行为。

旧类的方法会直接调用，不再经过 `Api.__new__` 的框架响应转换。因此迁移阶段的 handler 应返回普通数据、`(body, status)` 或新版 `ResponseContext`，不要返回 Django/Flask/Bottle 原生 Response。

### 第三步：逐个接口改成类型契约

旧配置：

```python
{
    "url": "users/<id>",
    "class": UserApi,
    "methods": {
        "PATCH": [
            {"name": "id", "type": int, "required": True},
            {"name": "name", "type": str, "required": True, "min": 2},
        ]
    },
}
```

推荐改为：

```python
from typing import Annotated
from pydantic import BaseModel, Field
from api_shop import ApiRegistry, Body, Path


class PatchUserBody(BaseModel):
    name: str = Field(min_length=2)


class PatchUserInput(BaseModel):
    id: Annotated[int, Path()]
    body: Annotated[PatchUserBody, Body()]


api = ApiRegistry()


@api.route(
    "/users/<int:id>",
    methods=["PATCH"],
    input=PatchUserInput,
    response={200: UserOutput, 404: ErrorOutput},
)
async def patch_user(ctx, data):
    ...
```

建议优先迁移：认证接口、包含敏感字段的响应、同名多来源参数、动态路由，以及内部使用 `api_run` 的接口。

### 第四步：替换 hook 和内部接口调用

`before_running` / `after_running` 改成 middleware：

```python
async def authenticate(ctx, call_next):
    ctx.state["user"] = await load_user(ctx.headers)
    response = await call_next(ctx)
    response.headers["X-Service"] = "accounts"
    return response


dispatcher = Dispatcher(api, middleware=[authenticate])
```

原 `api_run` 如果表达的是共享业务逻辑，应抽成普通 service 函数，由两个 handler 共同调用；只有确实需要完整 API 校验链时，才构造 `RequestContext` 调用 dispatcher。

### 第五步：锁定 OpenAPI 并移除 legacy

迁移完成后：

1. 保存一次 OpenAPI 3.1 输出作为契约基线。
2. 对比迁移前后的状态码、错误结构和响应字段。
3. 删除 `api_shop.legacy` 导入及旧 conf。
4. 删除旧文档和 mock 路由，按宿主系统的认证策略暴露 OpenAPI。

## 回归检查清单

- 路径、query、body 中的同名字段是否符合预期。
- 列表 query 是否仍以重复键传递，例如 `tag=a&tag=b`。
- bool 客户端是否发送了旧式的 `yes/no/on/off`。
- 所有业务状态码是否出现在 `response={...}` 中。
- 响应模型是否只包含允许公开的字段。
- middleware 顺序以及异常是否产生预期错误码。
- 动态路由是否使用正确 converter，是否与静态路由冲突。
- 同步代码是否错误地在 event loop 中调用 `dispatch()`。
