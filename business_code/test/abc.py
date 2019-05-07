# api-shop automatically inserts code
from src.api_shop import Api


class api_login(Api):
    """微信账户登录"""
    pass
    def post(self, request, data):
        """ todo:
        api-shop automatically inserts code
        data.username # 用户名
        data.ddd # 日期
        """
        print(data)
        # return
        return {'msg':'test'},400
        return 11
