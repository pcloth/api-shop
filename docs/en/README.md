---
home: true
heroImage: /hero.png
actionText: start →
actionLink: /start/
features:
- title: 简洁
  details: 根据一个list对象参数表来生成api接口。
- title: 省心
  details: 自动校验参数、自动转换参数格式、简化业务代码、自动生成文档和mock工具
- title: 省时
  details: 外部和内部均可复用业务代码
footer: MIT Licensed | Copyright © 2019 Pcloth
---

## **core function:**
1. Configuration api generation.
2. Automatically verify the data submitted by the request and convert it to the specified format, supporting: int, float, list, dict, set, tuple, bool
3. Automatically generate api documents and provide a web page for query and mock data presentation.
4. Compatible with `django` , `flask` , `bottle` (if you don't specify a frame, the frame is recognized by default in this order)
5. Automatically generate the interface `skeleton file` function (please open it carefully).
6. Custom format converter, data_format.datetime format conversion class; '2019-01-18 23:25:25' to datetime
7. Multi-language support, also supports custom language packs.
8. The documentation supports hot overloading.
9. The default value supports method functions.
10. Support url contains parameters, such as ```/api/user/<id>```, and set its rules when configuring the parameters parameter.
11. Support multiple url binding an interface
12. Support for options for specifying parameters, for example: [1,4,7], receiving a parameter other than this list will trigger bad_request
