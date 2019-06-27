api-shop v1.9.1
===============

`Online Documents <https://pcloth.github.io/api-shop/index.html>`_
------------------------------------------------------------------

api-shop：一个易用的、快速的restful-api接口工具包，兼容：django / flask / bottle

一切只为少加班。

.. image:: https://pcloth.github.io/api-shop/assets/img/demo.7342f254.png

**核心功能：**
--------------


#. 配置化api生成。
#. 自动校验request提交的数据，并转换成指定格式，支持：int，float，list，dict，set，tuple，bool
#. 自动生成api文档，并提供一个web页面可供查询和mock数据演示。
#. 兼容 ``django`` , ``flask`` , ``bottle`` (如果不指定框架，默认按这个顺序识别框架)
#. 自动生成接口\ ``骨架文件``\ 功能（请谨慎开启）。
#. 自定义格式转换器，data_format.datetime格式转换类；'2019-01-18 23:25:25' to datetime
#. 多国语言支持，也支持自定义语言包。
#. 文档热重载。
#. 默认值支持方法函数。
#. 支持url中包含参数，例如 ``/api/user/<id>``\ ，并且在配置methods参数的时候设置它的规则。
#. 支持多url绑定一个接口
#. 支持指定参数的可选项，例如：[1,4,7]，收到这个列表之外的参数就会触发bad_request
#. 可以在代码中直接调用Api业务代码：\ ``get_api_result_json``\ 和\ ``get_api_result_response``

`Online Documents <https://pcloth.github.io/api-shop/index.html>`_
------------------------------------------------------------------