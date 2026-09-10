---
prev:
    text: 首页
    link: /
next:
    text: 快速上手
    link: /start/
lastUpdated: true
---

# 设计与生命周期

## 为什么重新设计

1.x 同时负责配置解析、框架识别、路由分发、文档渲染和响应构造。它可以快速启动项目，但模块级全局状态会让多应用、并发测试和混合框架变得不可预测，字典配置也难以获得静态检查。

2.0 将职责拆成三层：

- `ApiRegistry`：声明路由和输入/响应契约，启动时编译为只读表。
- `Dispatcher`：匹配路由、绑定参数、执行中间件与 handler、校验响应。
- adapter：将宿主请求转换为 `RequestContext`，将 `ResponseContext` 转回框架响应。

核心包不会自动探测 Web 框架，也不会在运行时生成或修改业务源码。

## 请求生命周期

1. adapter 从挂载前缀中取出相对路径，并分别读取 headers、query、cookies、body、form 和 files。
2. registry 按“静态段、受限动态段、普通动态段、path 段”的顺序匹配。
3. dispatcher 根据字段上的来源标记取值，再交给 Pydantic 校验和转换。
4. middleware 依次执行，最终调用同步或异步 handler。
5. handler 结果按当前 HTTP 状态对应的响应模型校验并过滤字段。
6. adapter 把统一响应转换为宿主框架响应。

## 实例隔离

每个 `Dispatcher` 都持有自己的只读 registry、中间件和 logger，不依赖模块级 framework 或 singleton：

```python
public_dispatcher = Dispatcher(public_api, middleware=[request_log])
admin_dispatcher = Dispatcher(admin_api, middleware=[authenticate_admin])
```

两个实例可以挂载在不同前缀，测试时也不会互相覆盖。

## Rust 与性能

参数校验使用 Pydantic v2，其底层 `pydantic-core` 已由 Rust 实现。安装 `api-shop[fast]` 后，JSON 响应会优先使用 `orjson`，不可用时自动回退到标准库。

项目提供路由基准脚本。自研 Rust matcher 只有在与 Python 实现语义完全一致、且端到端 dispatch 提升达到 15% 后才会成为可选扩展；2.0 首版不要求用户安装 Rust。
