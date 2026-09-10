---
title: 校验与自定义类型
---

# 校验与自定义类型

2.0 使用 Pydantic v2 代替 1.x 的 `data_format` 和手写 `min/max/options` 转换器。

## 长度和数值范围

```python
from typing import Annotated
from pydantic import BaseModel, Field
from api_shop import Query


class ListInput(BaseModel):
    keyword: Annotated[str, Query(), Field(min_length=2, max_length=50)]
    page: Annotated[int, Query(), Field(ge=1, le=1000)] = 1
```

也可以把约束直接写在字段赋值上：

```python
class ListInput(BaseModel):
    keyword: Annotated[str, Query()] = Field(min_length=2, max_length=50)
```

`ge=0`、`le=0` 会正常生效，不再受 1.x truthy 判断影响。

## 可选项

```python
from typing import Literal


class SortInput(BaseModel):
    order: Annotated[Literal["created", "name"], Query()] = "created"
```

## 日期、邮箱、URL 和 UUID

```python
from datetime import date, datetime
from uuid import UUID
from pydantic import AnyHttpUrl, EmailStr


class ProfileInput(BaseModel):
    user_id: Annotated[UUID, Path()]
    birthday: Annotated[date | None, Query()] = None
    at: Annotated[datetime | None, Query()] = None
    email: Annotated[EmailStr, Query()]
    callback: Annotated[AnyHttpUrl, Query()]
```

部分 Pydantic 类型需要安装其可选依赖，例如 `EmailStr` 通常需要 `email-validator`。

## 自定义校验

```python
from typing import Annotated
from pydantic import AfterValidator


def valid_username(value: str) -> str:
    if not value.replace("_", "").isalnum():
        raise ValueError("username contains invalid characters")
    return value


Username = Annotated[str, AfterValidator(valid_username)]


class UserInput(BaseModel):
    username: Annotated[Username, Query()]
```

复杂的多字段规则可以使用 Pydantic `field_validator` 或 `model_validator`。

## bool 规则

api-shop 在交给 Pydantic 前会对顶层 bool 字段执行严格转换，只接受：

- Python `True` / `False`
- 整数 `1` / `0`
- 字符串 `"true"` / `"false"` / `"1"` / `"0"`，大小写不敏感

`yes`、`no`、`on`、空字符串或其他文本都会返回 422。

::: warning 1.x data_format
`data_format.datetime`、`data_format.regex` 等仅保留给 legacy API。新代码使用 Pydantic 标准类型、`Field` 和 validator。
:::
