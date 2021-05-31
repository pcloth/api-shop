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
1. Configuration API generation.
2. Automatically verify the data submitted by request, and convert it to the specified format, support: int, float, list, dict, set, tuple, bool
3. Automatically generate API documents and provide a web page for query and mock data presentation.
4. Compatible with `django`, `flask`, `bottle` (if no frame is specified, frames are recognized in this order by default)
5. Automatically generate the interface `skeleton file` function beta (please turn it on carefully).
6. Custom format converter, data_format.datetime format conversion class; '2019-01-18 23:25:25' to datetime
7. Support regular format check.
8. Multi-language support, also supports custom language packs.
9. Hot reloading of documents.
10. The default value supports method functions.
11. Support url contains parameters, such as `/api/user/<id>`, and set its rules when configuring method parameters.
12. Support multiple url binding an interface
13. Supports options for specifying parameters, for example: [1,4,7], bad_request will be triggered when parameters outside this list are received
14. You can directly call the Api business code in the code: `api_run` (`get_api_result_json` and `get_api_result_response` will be removed)
