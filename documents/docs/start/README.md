# 快速上手

## 安装

核心只依赖 Pydantic v2：

```bash
python -m pip install "api-shop>=2,<3"
```

根据宿主框架安装 extra：

```bash
python -m pip install "api-shop[django]>=2,<3"
python -m pip install "api-shop[flask]>=2,<3"
python -m pip install "api-shop[bottle]>=2,<3"
python -m pip install "api-shop[fast]>=2,<3"     # 可选 orjson
```

api-shop 2.0 要求 Python 3.10 或更高版本。

## 声明请求和响应

```python
from typing import Annotated

from pydantic import BaseModel, Field
from api_shop import ApiRegistry, Body, Header, Path, Query


class CreateUserBody(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: str


class CreateUserInput(BaseModel):
    team_id: Annotated[int, Path()]
    notify: Annotated[bool, Query()] = False
    token: Annotated[str, Header(alias="Authorization")]
    body: Annotated[CreateUserBody, Body()]


class UserOutput(BaseModel):
    id: int
    name: str
    email: str


api = ApiRegistry()


@api.route(
    "/teams/<int:team_id>/users",
    methods=["POST"],
    input=CreateUserInput,
    response={201: UserOutput},
    tags=["users"],
    name="create_user",
)
async def create_user(ctx, data):
    user = await save_user(data.team_id, data.body)
    return user, 201
```

创建 `Dispatcher` 时 registry 会立即编译。缺少参数来源、路径参数不对应、未知 converter 或歧义路由都会在启动时失败：

```python
from api_shop import Dispatcher

dispatcher = Dispatcher(api)
```

## 挂载到宿主框架

### 通用 ASGI

```python
from api_shop.adapters import ASGIAdapter

application = ASGIAdapter(dispatcher, prefix="/api")
```

### Flask

```python
from flask import Flask
from api_shop.adapters import mount_flask

app = Flask(__name__)
mount_flask(app, dispatcher, prefix="/api")
```

### Django

```python
from api_shop.adapters import django_urlpatterns

urlpatterns = django_urlpatterns(dispatcher, prefix="api")
```

也可以将返回的列表追加到已有 `urlpatterns`。

### Bottle

```python
from bottle import Bottle
from api_shop.adapters import mount_bottle

app = Bottle()
mount_bottle(app, dispatcher, prefix="/api")
```

## 直接调度

测试或内部调用可以绕过宿主框架：

```python
from api_shop import RequestContext

response = dispatcher.dispatch(RequestContext(
    method="POST",
    path="/teams/7/users",
    query={"notify": "true"},
    headers={"Authorization": "Bearer example"},
    body={"name": "Ada", "email": "ada@example.com"},
))
```

异步上下文中必须使用：

```python
response = await dispatcher.dispatch_async(request_context)
```

不要在正在运行的 event loop 内调用同步 `dispatch()`。
