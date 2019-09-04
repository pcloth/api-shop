# changelog


---
> 2019-09-04 
>
> var 1.9.3
- Refactoring the document template page, adding front-end routing support, and the url contains the current interface information for easy communication.
---

---
> 2019-06-27
>
> var 1.9.1
- Add the `debug` parameter, the default is True. When it is True, the auto-fill function may take effect (of course, the corresponding parameters must also be enabled.)
- If the business code fails to load after opening, an error will be thrown and the program will be interrupted.
---


---
> 2019-05-07
>
> var 1.9.0
- Add code reuse methods: `get_api_result_json` and `get_api_result_response`
- Can directly call the return value of the api
---

---
> 2019-04-03
>
> var 1.8.0
- Support for options for specifying parameters, for example: [1,4,7], receiving a parameter other than this list will trigger bad_request
---

---
> 2019-04-03
>
> var 1.7.3
- Added support for multiple interfaces to support multiple url bindings.
```python
{
        'url': ['weixin', 'weixin/<name>/<id>'],
        'class': 'business_code.views.test',
        'name': 'Account login',
        'methods': {
            'POST': [
                {'name': 'id', 'type': bool, 'required': True, 'description': 'user id'},
                {'name': 'name', 'type': str, 'min':4,'required': True,'description': 'username'},
            ],
        }
    },
```
---

---
> 2019-03-15
>
> var 1.7.2
- Further abstract optimization code to facilitate the addition of new framework support.
- Added support for the bottle frame.
- Add the bad_request_error_status parameter. When bad_request==False, bad_request_error_status is the custom error status information returned to the bad request.
---

---
> 2019-03-14
>
> ver 1.7.1
- Optimize the framework loading logic, the default loading framework order ```django``` -> ```flask```; add configuration parameters directly to specify the framework.
- Optimize some of the regular processing logic.
---

---
> 2019-03-12
>
> ver 1.7.0
- Added automatic generation of interface skeleton files based on configuration files: When you add conf content, api-shop will automatically create based on its contents.
  Directory, file, import module, create classes and methods, and create notes based on parameters configured by the interface to reduce the amount of code you have.
- E.g:
```python
af = ApiShop(conf,
    {
        'lang': 'zh',
        'name_classification': ['WeChat', 'Account'],
        'url_classification': ['weixin', 'login'],
        'auto_create_folder': True, # Create folder automatically
        'auto_create_file': True, # Automatically create files
        'auto_create_class': True, # automatically create class
        'auto_create_method': True, # automatic creation method
    })
```

Generated file
```python
# api-shop automatically inserts code
from api_shop import Api

class api_login(Api):
    """WeChat account login """
    def post(self, request, data):
        """ todo:
        Api-shop automatically inserts code
        Data.username # username
        Data.ddd # Date
        """
        pass
```
---


---
> 2019-03-06
>
> ver 1.6.7
- Add url parameter support
- E.g:
```python
conf = [{
        'url': 'weixin/<name>/<id>',
        'class': 'business_code.views.test',
        'name': 'test api',
        'methods': {
            'POST': [
                {'name': 'id', 'type': int, 'required': True, 'description': 'user id'},
                {'name': 'name', 'type': str, 'min':4,'required': True,'description': 'username'},
            ],
        }
    },]
```
---

---
> 2019-02-25
>
> ver 1.6.5
- Add empty Response support, Api method can not return any value
- Added support for bool parameter types
- Interface documentation supports filtering (options are required)
---