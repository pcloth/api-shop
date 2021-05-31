# api-shop  ![PyPI](https://img.shields.io/pypi/v/api-shop?logo=api-shop) ![PyPI - Downloads](https://img.shields.io/pypi/dm/api-shop)

## [Online Documents](https://pcloth.gitee.io/api-shop/)
## [在线文档](https://pcloth.gitee.io/api-shop/)

> ### api-shop：一个易用的、快速的restful-api接口工具包，兼容：`django` / `flask` / `bottle`。
> ### `一切只为少加班。`

## **demo 图片**

![demo](/static/demo.png)


## **核心功能：**
1. 配置化api生成。
2. 自动校验request提交的数据，并转换成指定格式，支持：int，float，list，dict，set，tuple，bool
3. 自动生成api文档，并提供一个web页面可供查询和mock数据演示。
4. 兼容 `django` , `flask` , `bottle` (如果不指定框架，默认按这个顺序识别框架)
5. 自动生成接口`骨架文件`功能（请谨慎开启）。
6. 自定义格式转换器，data_format.datetime格式转换类；'2019-01-18 23:25:25' to datetime
7. 支持正则格式校验。
8. 多国语言支持，也支持自定义语言包。
9. 文档热重载。
10. 默认值支持方法函数。
11. 支持url中包含参数，例如 `/api/user/<id>`，并且在配置methods参数的时候设置它的规则。
12. 支持多url绑定一个接口
13. 支持指定参数的可选项，例如：[1,4,7]，收到这个列表之外的参数就会触发bad_request
14. 可以在代码中直接调用Api业务代码：`api_run`（将移除`get_api_result_json`和`get_api_result_response`）
15. 添加返回数据文档生成功能。



## [Online Documents](https://pcloth.gitee.io/api-shop/)
## [在线文档](https://pcloth.gitee.io/api-shop/)


