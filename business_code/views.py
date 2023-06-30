# 业务模块，flask和django写法一样
from src.api_shop import Api, ApiShop, single_apishop
from src.api_shop.func import model


class api_login(Api):
    # af = ApiShop()
    # print(af,'af')
    def post(self,request,data=None):
        '''api登陆接口，方便微信用户绑定账户'''
        print(data)
        return {'status': 'success'}


class test(Api):
    def get(self, request, data=None):
        print(data)
        a={'a':2 ,'b':6}
        # return
        # # return 'err',400
        # return {'msg':'你删除了id={}的账号'.format(data.id)}
        return {'msg':'GET信息','data':data}

    def post(self, request, data=None):
        print('test', data)
        return {'msg':'POST信息','data':data}
