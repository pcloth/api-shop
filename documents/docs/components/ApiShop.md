---
title: ApiRegistry 与 Dispatcher
---

# ApiRegistry 与 Dispatcher

## ApiRegistry

`ApiRegistry` 在声明阶段可变，在 `compile()` 或创建 `Dispatcher` 后变为只读。编译后继续注册路由会抛出 `RuntimeError`。

```python
api = ApiRegistry()


@api.route(
    "/users/<uuid:user_id>",
    methods=["GET"],
    input=GetUserInput,
    response={200: UserOutput, 404: ErrorOutput},
    tags=["users"],
    name="get_user",
)
async def get_user(ctx, data):
    ...


api.compile()
```

### route 参数

| 参数 | 说明 |
| --- | --- |
| `path` | 相对路径；首尾 `/` 会规范化 |
| `methods` | 至少一个 HTTP method，不区分输入大小写 |
| `input` | Pydantic `BaseModel` 子类；无参数接口可以省略 |
| `response` | 单一响应类型，或 `{状态码: 类型}` 映射 |
| `tags` | OpenAPI 标签 |
| `name` | OpenAPI operationId；默认使用 handler 名称 |

### 路由 converter

| 写法 | Python 类型 | 匹配范围 |
| --- | --- | --- |
| `<name>` / `<str:name>` | `str` | 单个非空路径段 |
| `<int:id>` | `int` | 非负整数 |
| `<uuid:id>` | `UUID` | 标准 UUID |
| `<slug:name>` | `str` | 字母、数字、下划线和连字符 |
| `<path:rest>` | `str` | 包含 `/` 的剩余路径，必须位于最后 |

静态段优先于受限动态段，普通动态段其次，`path` 最后。相同 method 下等价的动态路由会在编译时被拒绝。

## Dispatcher

```python
dispatcher = Dispatcher(
    api,
    middleware=[request_log, authenticate],
    logger=logger,
)
```

同步环境调用 `dispatcher.dispatch(ctx)`，异步环境调用 `await dispatcher.dispatch_async(ctx)`。同步方法不能在正在运行的 event loop 内使用。

handler 支持三种返回方式：

```python
return {"id": 1}                         # 默认 200
return {"id": 1}, 201                    # body, status
return ResponseContext(body=data, status=202, headers={"X-Job": "1"})
```

只要声明了 `response`，返回状态就必须出现在映射中，body 也必须通过对应类型校验。失败时客户端只收到通用 500，具体校验信息写入 logger。

## Middleware

middleware 接收当前上下文和下游 callable：

```python
async def request_log(ctx, call_next):
    started = time.perf_counter()
    try:
        return await call_next(ctx)
    finally:
        logger.info("api request", extra={
            "request_id": ctx.request_id,
            "elapsed": time.perf_counter() - started,
        })
```

middleware 按声明顺序进入、反向退出。认证结果等请求级数据应放在 `ctx.state`，不要写全局变量。
