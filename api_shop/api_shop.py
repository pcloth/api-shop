'''
api 工厂
可以让用户用数据来配置api模块，并自动校验参数合法性和生成文档页面。
by pcloth
'''
import json, traceback

# django引入包
framework = None
stacks = traceback.extract_stack()#[0].filename
for stack in stacks:
    if 'django' in stack.filename:
        try:
            from django.http import JsonResponse, HttpResponse
            from django.shortcuts import render
            framework = 'django'
            break
        except:
            raise 'ApiFactory： django版本不兼容，推荐使用2.1版本，或者去修改JsonResponse, HttpResponse引入位置。'
if not framework:
    try:
        from flask import render_template_string,jsonify
        framework = 'flask'
    except:
        raise 'ApiFactory：目前只兼容django和flask。'
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



BAD_REQUEST = True

def dynamic_import(name):
    components = name.split('.')
    mod = __import__('.'.join(components[:-1]))
    for comp in components[1:]:
        if hasattr(mod,comp):
            mod = getattr(mod,comp)

    # mod = __import__(components[0])
    # for comp in components[1:]:
    #     mod = getattr(mod, comp)
    return mod

class Namespace(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value

class ApiDataClass(Namespace):
    pass

def return_response(msg=None, status_code=400):
    # 返回错误信息
    if BAD_REQUEST:
        if framework == 'django':
            return HttpResponse(msg, status=status_code)
        if framework == 'flask':
            return jsonify({'msg':msg}),status_code
        raise '不支持的framework'
    else:
        if framework == 'django':
            return JsonResponse({'status': status_code, 'message': msg})
        if framework == 'flask':
            return jsonify({'msg':msg}),status_code
        raise '不支持的framework' 

class Api():
    '''制作api接口的最终方法时，请继承本类，用法类似Flask-RESTful的Resource
    例子：
    class youapi(Api):
        def get(self,request,data):
            # request 是当前的请求上下文
            # data 是被参数过滤器过滤并格式化后的请求附带数据
            return response
        def post(self,request,data):
            # 同上
        def put(self,request,data):
            # 同上
        def delete(self,request,data):
            # 同上
        def patch(self,request,data):
            # 同上
    '''
    def __new__(self,request,data=None):
        method = request.method.lower()
        if hasattr(self,method):           
            func = getattr(self,method)
            retdata = func(self,request,data)
            status_code = 200
            if type(retdata)==tuple and len(retdata)==2:
                ret = retdata[0]
                status_code = retdata[1]
            else:
                ret =retdata
            if framework == 'django':
                return JsonResponse(ret, status=status_code)
            if framework == 'flask':
                return jsonify(ret),status_code
            raise '不支持的framework'
        else:
            return return_response('没有这个 {} 方法。'.format(method))


class ApiShop():
    def __init__(self, conf, options=None):
        '''
        配置api工厂参数，格式如下：
        conf = [
            {
                'url': 'login',
                'class': 'account.views.api_login',
                'name': '账户登录',
                'methods': {
                    'POST': [
                        {'name':'username', 'type': str, 'required': True, 'min': 3, 'max': 24, 'description': '用户名'},
                        {'name':'password', 'type': str, 'required': True, 'min': 3, 'max': 24, 'description': '密码'},
                    ]
                }
            },
        ]

        options = {
            'base_url':'/api/',# 基础url，用以组合给前端的api url
            'document':BASE_DIR+'/api_shop/static/document.html' # 文档路由渲染的模板
        }
        '''
        if not framework:
            raise 'ApiFactory 不支持除了django和flask之外的其他框架！'

        if not options:
            self.options = {
                'base_url':'/api/', # 基础url，用以组合给前端的api url
                'bad_request':True, # 参数bad_request如果是真，发生错误返回一个坏请求给前端，否则都返回200的response，里面附带status=error和msg附带错误信息
            }
        else:
            self.options = options

        try:
            if self.options.get('document'):
                doc_file = open(self.options.get('document'),mode='r',encoding='utf-8')
            else:
                doc_file = open(BASE_DIR+'/api_shop/static/document.html',mode='r',encoding='utf-8')
            self.document = doc_file.read()
        except:
            self.document = '''<h1>没有找到文档模板</h1>'''


        global BAD_REQUEST
        BAD_REQUEST = self.options.get('bad_request',True)

        # 当前加载的url和function的字典
        self.url_dict = {}  
        # url方法字典
        self.url_methods = {}
        self.api_data = []
        

        self.conf = self.__make_model(conf)
        
        self.api_count = len(self.conf)

      
        
    def __class_to_json(self, methods):
        '''将python的数据对象类切换成字符串'''
        fix_list = ['str', 'list', 'dict', 'set', 'int', 'float', 'bool', 'complex']
        string = methods.__str__()
        for fix in fix_list:
            string = string.replace("<class '{}'>".format(fix), '"{}"'.format(fix))
        
        
        return eval(string)

    def __make_model(self, conf):
        # 将字符串里的function模块和函数加载进来，并写入到run_function字段方便调用。
        for i in range(len(conf)):
            model = dynamic_import(conf[i]['class'])
            self.url_dict.update({
                conf[i]['url']: model,
            })
            self.url_methods.update({
                conf[i]['url']: conf[i]['methods'],
            })
            conf[i]['methods'] = self.__class_to_json(conf[i]['methods'])
            
            if hasattr(model,'__doc__'):
                conf[i]['document'] = getattr(model,'__doc__')

        return conf

    def __not_find_url_function(self, request):
        # 如果是django
        return JsonResponse({'status': 'error', 'msg': '没有这个接口'})

    def __find_api_function(self, url):
        # 查找api所指向的模块
        if(type(url)==tuple and len(url)>0):
            model = self.url_dict.get(url[0])
            if model:
                return model
            else:
                return self.__not_find_url_function

    def __find_api_methons(self, url):
        # 查找api所指向的方法
        if(type(url)==tuple and len(url)>0):
            return self.url_methods.get(url[0])

    def get_parameter(self, request):
        # 获取参数
        data = {}
        # 获取django的request数据
        if framework=='django':
            if request.GET:
                data.update(request.GET.dict())
            elif request.POST:
                data.update(request.POST.dict())
            elif request.is_ajax():
                # axios payload 方式传递数据
                # 如果使用axios，必须指定'X-Requested-With'='XMLHttpRequest'
                data.update(json.loads(request.body))
            else:
                try:
                    data.update(json.loads(request.body))
                except:
                    pass
        if framework=='flask':
            if request.args:
                data.update(request.args.to_dict())
            if request.form:
                data.update(request.form.to_dict())
            if request.json:
                data.update(request.json)
        return data

    def __verify(self, conf, name, value):
        # 校验数据并转换格式
        required_ = conf.get('required')
        type_ = conf.get('type')
        min_ = conf.get('min')
        max_ = conf.get('max')
        default_ = conf.get('default')

        # 检查默认值
        if not value and default_:
            value = default_
        # 检查必要值
        if required_ == True and not value:
            return '必要参数 {} 缺失'.format(name), None
        # 检查并转换类型
        if type_ and type(value) != type_:
            try:
                value = type_(json.loads(value))
            except:
                return '参数 {} 必须是 {} '.format(name, type_), None
        # 检查最小值/长度
        if min_:
            if type(value) in [str, list, dict, set] and len(value) < min_:
                return '参数 {} 的最小长度是 {} '.format(name, min_), None
            if type(value) in [int, float, bool, complex] and value < min_:
                return '参数 {} 的最小值是 {} '.format(name, min_), None

        # 检查最大值/长度
        if max_:
            if type(value) in [str, list, dict, set] and len(value) > max_:
                return '参数 {} 的最大长度是 {} '.format(name, max_), None
            if type(value) in [int, float, bool, complex] and value > max_:
                return '参数 {} 的最大值是 {} '.format(name, max_), None
        return None, value

    def verify_parameter(self, request, par_conf):
        # 校验参数合法性，并转换成参数对象
        if type(par_conf) != list:
            return '错误的api factory 配置项目，methons必须装的list容器内。', None

        parameter = self.get_parameter(request)
        adc = ApiDataClass()
        errmsg = []
        # 从参数配置获取参数
        for line in par_conf:
            key = line['name']
            errmsg_, value = self.__verify(line, key, parameter.get(key))
            if errmsg_:
                errmsg.append(errmsg_)
            else:
                setattr(adc,key,value)
        return errmsg, adc
        
    def api_entry(self,request,*url):
        '''api入口'''
        model = self.__find_api_function(url)
        methons = self.__find_api_methons(url)
        
        if methons and methons.get(request.method):
            # 有配置方法和参数，校验参数合法性，并转换参数
            errmsg, data = self.verify_parameter(request, methons.get(request.method))
            if errmsg:
                return return_response(errmsg)
        else:
            return return_response('没有这个接口method')
   
        
        return model(request,data)

    def render_documents(self,request,*url):
        '''渲染文档'''
        if framework == 'django':
            return HttpResponse(content=self.document, content_type=None, status=200, reason=None, charset=None)
        elif framework == 'flask':
            return render_template_string('{% raw %}'+self.document+'{% endraw %}')

    def get_api_data(self, request, *url):
        '''返回给文档页面数据'''
        if framework == 'django':
            return JsonResponse({'data': self.conf,'options':self.options})
        elif framework == 'flask':
            return jsonify({'data': self.conf,'options':self.options})
        
 