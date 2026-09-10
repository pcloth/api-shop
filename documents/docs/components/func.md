---
title: OpenAPI 与 ORM
---

# OpenAPI 与 ORM

## 生成 OpenAPI 3.1

OpenAPI 从已编译 registry 生成，因此路径、参数来源和响应模型与运行时使用同一份契约：

```python
from api_shop import generate_openapi

schema = generate_openapi(
    api,
    title="Account API",
    version="2.0.0",
    description="Account service endpoints",
)
```

返回值是普通 dict，可以由宿主框架自行暴露：

```python
@app.get("/openapi.json")
def openapi_json():
    return schema
```

生产环境是否公开文档和 schema 应由宿主应用决定。内部接口建议鉴权或完全关闭，不要把 API 文档页面当成权限边界。

当前生成内容包括：

- OpenAPI 3.1 版本和 info。
- 路径、method、operationId 和 tags。
- path/query/header/cookie 参数。
- JSON body、multipart form/file。
- 按状态码区分的响应 schema。

## Django ORM DTO

```python
from api_shop.orm import DjangoModelInspector

UserOutput = DjangoModelInspector().create_dto(
    User,
    ["id", "display_name", "created_at"],
    name="UserOutput",
)
```

## SQLAlchemy DTO

```python
from api_shop.orm import SQLAlchemyModelInspector

UserOutput = SQLAlchemyModelInspector().create_dto(
    User,
    ["id", "display_name", "created_at"],
    name="UserOutput",
)
```

生成的 DTO 开启了 `from_attributes=True`，可以校验 ORM 实例：

```python
return UserOutput.model_validate(user)
```

## 安全限制

- 字段列表必须显式提供且不能为空。
- `password`、`password_hash`、`secret`、`token`、`api_key` 不允许自动生成，确需公开时必须手写 DTO。
- Django relationship 字段不会自动展开。
- SQLAlchemy inspector 只读取 column，不读取 relationship。
- inspector 不执行查询、不写库，也不会自动保存请求数据。

DTO 应被视为公开接口的一部分。数据库字段变更不应自动改变 API；需要更复杂的别名、计算字段或嵌套关系时，请手写 Pydantic 输出模型。
