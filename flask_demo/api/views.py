from api_shop import Api

# Create your views here.


class api_login(Api):
    '''api登陆接口，方便微信用户绑定账户'''
    def post(self,request,data=None):
        return {}
        
        username = data.username
        password = data.password
        if len(username)<=4:
            return {'msg':'找不到该用户'},400

        
        return {'status': 'success', 'username': username}


class test(Api):
    '''健康预测计算：
    1
    2
    3
    4
    '''
    def get(self, request, data=None):
        '''get方法的文档'''
        return {'msg':data}
    def delete(self, request, data=None):
        '''del文档
        ceshi #'''
        return {'msg':'你删除了id={}的账号'.format(data.id)}

    def post(self, request, data=None):
        '''post文档'''
        return {'msg':'你提交了信息','data':data}