
api-shop 
.. image:: https://img.shields.io/pypi/v/api-shop?logo=api-shop
   :target: https://img.shields.io/pypi/v/api-shop?logo=api-shop
   :alt: PyPI
 
.. image:: https://img.shields.io/pypi/dm/api-shop
   :target: https://img.shields.io/pypi/dm/api-shop
   :alt: PyPI - Downloads

============================================================================================================================================================================================================================================================================================

`Online Documents <https://pcloth.gitee.io/api-shop/>`_
-----------------------------------------------------------

`在线文档 <https://pcloth.gitee.io/api-shop/>`_
---------------------------------------------------

..

   api-shop：一个易用的、快速的 restful-api 接口工具包，兼容：\ ``django`` / ``flask`` / ``bottle``\ 。
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   ``一切只为少加班。``
   ^^^^^^^^^^^^^^^^^^^^^^^^


**demo 图片**
-----------------


.. image:: /static/demo.png
   :target: /static/demo.png
   :alt: demo


**核心功能：**
------------------


#. 配置化 api 生成。
#. 自动校验 request 提交的数据，并转换成指定格式，支持：int，float，list，dict，set，tuple，bool、自定义格式转换器和正则格式校验
#. 自动生成 api 文档，并提供一个 web 页面可供查询和 mock 数据演示。
#. 兼容 ``django`` , ``flask`` , ``bottle`` (如果不指定框架，默认按这个顺序识别框架)
#. 自动生成接口\ ``骨架文件``\ 功能 beta（请谨慎开启）。
#. 多国语言支持，也支持自定义语言包。
#. 文档热重载。
#. 默认值支持方法函数。
#. 支持 url 中包含参数，例如 ``/api/user/<id>``\ ，并且在配置 methods 参数的时候设置它的规则。
#. 支持多 url 绑定一个接口
#. 支持指定参数的可选项，例如：[1,4,7]，收到这个列表之外的参数就会触发 bad_request
#. 可以在代码中直接调用 Api 业务代码：\ ``instance.api_run``
#. 支持在 Api 类中定义 response_docs 来制作返回值文档，并支持模型字段引入；以及模型部分字段引入类：ApiResponseModelFields
#. 添加了全局单例类 SingleApiShop，用来替代 ApiShop，优点是支持用户封装后覆盖单例

`Online Documents <https://pcloth.gitee.io/api-shop/>`_
-----------------------------------------------------------

`在线文档 <https://pcloth.gitee.io/api-shop/>`_
---------------------------------------------------
