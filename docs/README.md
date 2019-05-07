---
home: true
heroImage: /hero.png
actionText: 快速上手 →
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

## **核心功能：**
1. 配置化api生成。
2. 自动校验request提交的数据，并转换成指定格式，支持：int，float，list，dict，set，tuple，bool
3. 自动生成api文档，并提供一个web页面可供查询和mock数据演示。
4. 兼容 `django` , `flask` , `bottle` (如果不指定框架，默认按这个顺序识别框架)
5. 自动生成接口`骨架文件`功能（请谨慎开启）。
6. 自定义格式转换器，data_format.datetime格式转换类；'2019-01-18 23:25:25' to datetime
7. 多国语言支持，也支持自定义语言包。
8. 文档热重载。
9. 默认值支持方法函数。
10. 支持url中包含参数，例如 `/api/user/<id>`，并且在配置methods参数的时候设置它的规则。
11. 支持多url绑定一个接口
12. 支持指定参数的可选项，例如：[1,4,7]，收到这个列表之外的参数就会触发bad_request
13. 可以在代码中直接调用Api业务代码：`get_api_result_json`和`get_api_result_response`
