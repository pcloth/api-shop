---
home: true
heroImage: /logo.png
actionText: Quick start →
actionLink: /en/start/
features:
- title: concise
  details: The api interface is generated according to a list object parameter table.
- title: auto
  details: Automatically validate parameters, automatically convert parameter formats, auto-generate documents, and mock tools
- title: quick
  details: Simplify business code, both externally and internally. Everything is only for less work overtime.
footer: MIT Licensed | Copyright © 2019 Pcloth
---

![PyPI](https://img.shields.io/pypi/v/api-shop?logo=api-shop) ![PyPI - Downloads](https://img.shields.io/pypi/dm/api-shop)

## **core function:**
1. Configuration api generation.
2. Automatically verify the data submitted by the request and convert it to the specified format, supporting: int, float, list, dict, set, tuple, bool
3. Automatically generate api documents and provide a web page for query and mock data presentation.
4. Compatible with `django` , `flask` , `bottle` (if you don't specify a frame, the frame is recognized by default in this order)
5. Automatically generate the interface `skeleton file` function (please open it carefully).
6. Custom format converter, data_format.datetime format conversion class; '2019-01-18 23:25:25' to datetime
7. Multi-language support, also supports custom language packs.
8. The document is hot and heavy.
9. The default value supports method functions.
10. Support url contains parameters, such as `/api/user/<id>`, and set its rules when configuring the parameters parameter.
11. Support multiple url binding an interface
12. Support for options for specifying parameters, for example: [1,4,7], receiving a parameter other than this list will trigger bad_request
13. The Api business code can be called directly in the code: `get_api_result_json` and `get_api_result_response`
14. Quickly export the ORM mold to json data (`func.model.dumps` and `func.model.models_to_list`), or you can directly update the ORM mold (` func.model.loads`) with dict data.
