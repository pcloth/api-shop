# api-shop automatically inserts code
from src.api_shop import Api, ApiResponseModelFields
from src.api_shop import get_api_result_json
from flask_demo.models import User
class tt(Api):
    pass

class api_login(Api):
    """微信账户登录"""
    response_docs = {
        'get':{
            'test':{User.name,User.email},
            'results':{'test:ss:dddd',ApiResponseModelFields(User,['id',User.name,'email'])},
        }
    }

    def post(self, request, data):
        """ todo:
        api-shop automatically inserts code
        data.username # 用户名
        data.ddd # 日期
        """
        from flask_demo.views import af
        ret,code = af.api_run(request, 'weixin/test/1', 'POST')
        print(ret,code,'>>>>')
        return ret,code
        
    def get(self, request, data):
        """ todo:
        api-shop automatically inserts code
        data.username # 用户名
        data.ddd # 日期
        """
        get_api_result_json(tt, 'GET', request)
        # from flask_demo.views import af
        # ret,code = af.api_run(request, 'weixin/name/2', 'POST')
        # ret,code = self.api_run(request, 'weixin/name/2', 'POST')
        # print(ret,code,'>>>>')
        # return ret,code
