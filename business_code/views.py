# 业务模块，flask和django写法一样
from api_shop import Api

class api_login(Api):
    def post(self,request,data=None):
        '''api登陆接口，方便微信用户绑定账户'''
        username = data.username
        password = data.password
        if len(username)<=4:
            return {'msg':'找不到该用户'},400

        
        return {'status': 'success', 'username': username}


class test(Api):
    def delete(self,request,data=None):
        return {'msg':'你删除了id={}的账号'.format(data.id)}

    def post(self,request,data=None):
        return {'msg':'你提交了信息','data':data}

    