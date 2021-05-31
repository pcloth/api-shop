#!/usr/bin/env python3

'''
api 工厂
可以让用户用数据来配置api模块，并自动校验参数合法性和生成文档页面。
by pcloth
'''
import json, traceback, os, re, time, importlib

from .i18n import i18n_init
from .__init__ import __version__
from .url_parse import parse_rule
from .autofill import auto_fill,check_fill_methods
from werkzeug.local import LocalStack, LocalProxy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
i18 = i18n_init('zh')
_ = i18._

class Namespace(dict):
    def __getattr__(self, name):
        if name in self.keys():
            return self.get(name)
        else:
            raise AttributeError(_('no attributes found')+'{}'.format(name))

    def __setattr__(self, name, value):
        self.update({name:value})

class ApiInit(Namespace):
    '''接口初始化内，用于内部传递状态和配置加载多框架支持'''
    
# 框架基础配置
class FW(Namespace):
    # 配置框架需要使用的方法
    # 例如 if api.framework.name=='django':api.framework.JsonResponse
    # 就可以加载django的JsonResponse方法
    framework_models = {
        'django': {
            'django.http': ['JsonResponse', 'HttpResponse'],
        },
        'flask': {
            'flask': ['render_template_string','jsonify']
        },
        'bottle':{
            'bottle': ['template', 'HTTPResponse']
        }
    }
    framework_order = ['django', 'flask', 'bottle']

    framework_return = {
        'django': {
            'json': 'JsonResponse',
            'json_status_code_in_func':True,
            'http': 'HttpResponse',
            'http_status_code_in_func':True,
            'template': 'HttpResponse'
        },
        'flask': {
            'json': 'jsonify',
            'json_status_code_in_func':False,
            'http': None,
            'http_status_code_in_func':False,
            'template':None # 直接返回字符串
        },
        'bottle': {
            'json': 'HTTPResponse',
            'json_status_code_in_func': True, # json的状态码是否在方法内
            
            'http': 'HTTPResponse',
            'http_status_code_in_func':True, # http的状态码是否在方法内
            'template':None # 直接返回字符串
        },

    }

    def template(self,string):
        # 返回模板字符串
        if self.func_dict.get('template'):
            return self[self.func_dict.get('template')](string)
        else:
            return string

    def json(self, data,status_code=200):
        # 返回json字符串
        model_name = self.func_dict.get('json')
        flag = self.func_dict.get('json_status_code_in_func')
        if model_name:
            if flag:
                return self[model_name](data, status=status_code)
            else:
                return self[model_name](data), status_code
        else:
            return data,status_code

    def http(self, data, status_code=200):
        # 返回http
        model_name = self.func_dict.get('http')
        flag = self.func_dict.get('http_status_code_in_func')
        if model_name:
            if flag:
                return self[model_name](data, status=status_code)
            else:
                return self[model_name](data), status_code
        else:
            return data, status_code
            
        

    def load_fw_model(self, fwname, err_out=False):
        '''加载框架的方法'''
        if not self.framework_models.get(fwname):
            # 暂时不支持这个框架
            raise BaseException(_('Not support') + ' {} , ('.format(fwname) + _('supported framework as follows:') + ' , '.join(self.framework_order) + ')')
            
        current_fw = self.framework_models.get(fwname)
        haserr = False
        for path in current_fw:
            try:
                model = importlib.import_module(path)
            except:
                return
            
            for key in current_fw[path]:
                if not hasattr(model, key):
                    if err_out:
                        raise BaseException(_('Framework version is not compatible.'))
                    else:
                        haserr = True
                self[key] = getattr(model, key)
        if not haserr:
            self.name = fwname
        

    def __init__(self, fwname=None):
        self.name = None
        if fwname and type(fwname):
            self.load_fw_model(fwname.lower(), True)
        else:
            # 从默认顺序加载框架
            for fwname in self.framework_order:
                self.load_fw_model(fwname)
        if not self.name:
            if not fwname:
                raise BaseException(_('supported framework as follows:') + ' , '.join(self.framework_order))
            else:
                raise BaseException(_('Did not find the framework') + fwname)

        self.func_dict = self.framework_return.get(self.name)
       

class ApiResponseModelFields():
    '''用来包含模型的部分字段'''
    def __init__(self, model, fields:list=None, return_type=set):
        self.model = model
        self.type = return_type
        self.fwname = ''
        if 'django.db.models' in str(type(model)):
            self.fwname = 'django'
        elif 'sqlalchemy.orm' in str(type(model)):
            self.fwname = 'flask'
        self.fields = fields

    def __new__(cls, *args, **kwargs):
        model = kwargs.get('model')
        fields = kwargs.get('fields')
        if len(args)>=1:
            model = args[0]
        if len(args)>=2:
            fields = args[1]
        if fields:
            return object.__new__(cls)
        return model

    def get_fields(self):
        # 返回模型字段
        nameList = []
        for field in self.fields:
            key = None
            if type(field)==str:
                # 传入的字符串描述字段名称
                key = field
            elif self.fwname == 'django' and hasattr(field, 'field_name'):
                key = field.field_name
            elif self.fwname == 'flask' and hasattr(field, 'name'):
                key = field.name
            # raise BaseException(_('request.method and method are not equal'))
            if key:
                nameList.append(key)
        objList = []
        if self.fwname == 'django':
            for obj in self.model._meta.fields:
                if obj.name in nameList:
                    objList.append(obj)
        if self.fwname == 'flask':
            for obj in self.model.__table__._columns:
                if obj.name in nameList:
                    objList.append(obj)
        if self.type == set:
            return set(objList)
        return objList


api = ApiInit()

class ApiDataClass(Namespace):
    '''api-data类'''
    def __init__(self, data=None):
        if data:
            self.update(data)

    def dict(self):
        return self
    
    def to_dict(self):
        return self

    def get_json(self):
        return self

    def is_ajax(self):
        return False

def get_api_result_json(api_class, method, data=None, request=None, not200=True):
    '''
    直接调用api代码，并拿到返回json
        api_class 是业务api类的对象（不是实例）
        method 是请求方法,str格式
        data 是附加数据，dict格式
        request=None 是当前request,如果method和request.method不相同，请自己封装一个适合业务代码用的request，如果业务代码不用reqeust，请不要传入。
        not200=True 是允许status_code不等于200的结果，为False的时候，遇到200以外程序中断并抛错
    return json,status_code

    '''
    print(_('Please use the ApiShop.api_run instance method instead of this method, this method will be removed in later versions!!'))
    response = get_api_result_response(api_class, method, data,request,not200)
    if not response:
        # 无结果
        return None
    
    status_code = getattr(response, 'status_code')
    if not200==False and status_code!=200:
        raise BaseException(_('api-shop return result is not success.'))

    fw = api.get('framework')
    fwname = fw.get('name')
    
    if fwname == 'flask':
        if hasattr(response,'is_json') and response.is_json:
            ret = response.get_json()
        else:
            ret = None

    if fwname == 'django':
        if response.content:
            ret = json.loads(response.content)
        else:
            ret = None
    if fwname == 'bottle':
        ret = response.body

    return ret,status_code

def get_api_result_response(api_class, method, data=None, request=None, not200=True):
    '''
    绕过参数检查调用 api业务代码
    返回response
    api_class 是业务api类的对象（不是实例）
    method 是请求方法,str格式
    data 是附加数据，dict格式
    request=None 是当前request，业务代码如果不使用，可以不传递
    not200=True 是允许status_code不等于200的结果，为False的时候，遇到200以外程序中断并抛错
    返回值是 response
    '''
    print(_('Please use the ApiShop.api_run instance method instead of this method, this method will be removed in later versions!!'))
    d_ = ApiDataClass(data)

    fw = api.get('framework')
    fwname = fw.get('name')

    if request:
        if request.method != method:
            raise BaseException(_('request.method and method are not equal'))
    else:
        request = ApiDataClass(data)
        request.method = method
    
    
    tup = api_class(request,d_)

    if type(tup) == tuple:
        status_code = tup[1]
        res = tup[0]
    elif hasattr(tup,'status_code'):
        res = tup
        status_code = getattr(tup, 'status_code')
    if not200==False and status_code!=200:
        raise BaseException(_('api-shop return result is not success.'))
    return res

def return_response(msg=None, status_code=400):
    # 返回错误信息
    if msg:
        ret = {'msg': msg}
    else:
        ret = {}
    if not api.BAD_REQUEST:
        ret.update({'status': api.bad_request_error_status})
        status_code = 200
    return api.framework.json(ret, status_code)
class Api():
    '''制作api接口的最终方法时，请继承本类，用法类似Flask-RESTful的Resource
    例子：
    class your_api(Api):
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
    def __new__(self, request, data=None, json=None, method=None):
        if not method:
            method = request.method
        method = method.lower()
        if hasattr(self, method):
            func = getattr(self,method)
            retdata = func(self, request, data)
            status_code = 200
            if type(retdata)==tuple:
                ret = retdata[0]
                status_code = retdata[1] or 200
            else:
                ret = retdata
            # 允许返回空body
            if ret == None:
                ret = {}
            if json:
                return ret, status_code
            elif type(ret) == dict:
                return api.framework.json(ret, status_code)
            else:
                return api.framework.http(ret, status_code)
        else:
            return return_response(_('not found in conf')+ '{}'.format(method))


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
            
        }
        '''
        
        self.i18n = i18

        self.options = {
                'version':__version__,
                'base_url':'/api/', # 基础url，用以组合给前端的api url
                'bad_request': True,  # 参数bad_request如果是真，发生错误返回一个坏请求给前端，否则都返回200的response，里面附带status=error和msg附带错误信息
                'bad_request_error_status':'error',
                'document': BASE_DIR + '/api_shop/static/document.html',  # 文档路由渲染的模板
                'lang': 'en',
                'debug':True, # 默认开启调试信息
                'auto_create_folder': False,  # 自动创建文件夹
                'auto_create_file': False,  # 自动创建文件
                'auto_create_class': False,  # 自动创建类
                'auto_create_method': False,  # 自动创建方法
                
            }
        
        self.document_version = ''
        if options:
            self.options.update(options)
        try:
            if self.options.get('document'):
                self.document_name = self.options.get('document')
            else:
                self.document_name = BASE_DIR + '/api_shop/static/document.html'

            self.document_version = time.ctime(os.stat(self.document_name).st_mtime)
            self.document = open(self.document_name,mode='r',encoding='utf-8').read()
        except:
            self.document = '<h1>' + _('document template not found') + '</h1>'

        # 指定框架
        api.framework = FW(self.options.get('framework'))

        # 扩展语言包
        if type(self.options.get('lang_pack'))==dict:
            self.i18n.lang.update(self.options.get('lang_pack'))
        
        # 切换语言
        self.i18n.lang_name = self.options.get('lang')
        api.BAD_REQUEST = self.options.get('bad_request', True)
        api.bad_request_error_status = self.options.get('bad_request_error_status')


        # 当前加载的url和function的字典
        self.url_dict = {}  
        # url方法字典
        self.url_methods = {}
        self.api_data = []
        

        self.conf = self.__make_model(conf)
        
        self.api_count = len(self.conf)
        self.__init_url_rules()

        
    def __class_to_json(self, methods):
        '''将python的dict数据对象类切换成字符串'''
        string = str(methods) #.__str__()
        # 替换类名称
        class_list = re.compile(r"""<class '[\w|\.]*'>""",0).findall(string)
        for line in class_list:
            string = string.replace(line, "'{}'".format(line.split("'")[1]))

        # 替换其他对象名称
        others = re.compile(r'''<[\s|\S.]*>''', 0).findall(string)
        for line in others:
            try:
                string = string.replace(line, "'{}'".format(line.split(" ")[1]))
            except:
                string = string.replace(line, "'{}'".format(line))
            

        return eval(string)

    def __dynamic_import(self, thisconf):
        name = thisconf['class']
        if type(name)!=str:
            # 直接传入的对象
            return name
        components = name.split('.')
        path = '.'.join(components[:-1])
        try:
            exec('from {} import {}'.format(path, components[-1]))
            return eval(components[-1])
        except Exception as ie:
            if self.options.get('debug') == True:
                print('\n\n*******  api-shop errmsg  *******\n')
                print('currnet_api:\nurl: {}\nclass: {}\n'.format(thisconf.get('url'),thisconf.get('class')))
                traceback.print_exc()
                if auto_fill(thisconf, self.options) == True:
                    # 自动生成文件或者方法，成功后重试一次。
                    return self.__dynamic_import(thisconf)
                else:
                    os._exit(0)

    def __make_model(self, conf):
        # 将字符串里的function模块和函数加载进来，并写入到run_function字段方便调用。
        for i in range(len(conf)):
            # model = dynamic_import(conf[i]['class'])
            model = self.__dynamic_import(conf[i])
            model.api_run = self.api_run
            if type(conf[i]['class'])!=str:
                # 直接使用对象
                conf[i]['class'] = self.__class_to_json(conf[i]['class'])
            if type(conf[i]['url']) == list:
                # 支持多url表达方式
                for url in conf[i]['url']:
                    self.url_dict.update({
                        url: model,
                    })
                    self.url_methods.update({
                        url: conf[i]['methods'],
                    })
            else:
                self.url_dict.update({
                    conf[i]['url']: model,
                })
                self.url_methods.update({
                    conf[i]['url']: conf[i]['methods'],
                })
            conf[i]['methods'] = self.__class_to_json(conf[i]['methods'])
            
            if hasattr(model,'__doc__'):
                # 接口文档说明
                conf[i]['document'] = getattr(model, '__doc__')
            conf[i]['methods_documents'] = {} # 方法文档说明
            conf[i]['methods_return'] = {} # 方法返回值说明
            if hasattr(model, 'response_docs'):
                docs_obj = getattr(model, 'response_docs')
                response_docs = {}
                for key in ['get', 'post', 'delete', 'put', 'patch']:
                    if docs_obj.get(key):
                        nodes = docs_obj.get(key)
                        roots = self.__find_response_docs(key.upper(),nodes)
                        response_docs.update({key.upper():roots})
                conf[i]['methods_return'] = response_docs
            if self.options.get('auto_create_method'):
                check_fill_methods(model,conf[i])
            for key in ['get', 'post', 'delete', 'put', 'patch']:
                # 把业务类子方法的文档添加到数据表
                if hasattr(model, key):
                    mt = getattr(model, key)
                    if hasattr(mt, '__doc__'):
                        conf[i]['methods_documents'].update({key.upper(): getattr(mt, '__doc__')})

        return conf

    def __mk_django_model_field_doc(self,field):
        # 把django字段模型提取成文档字段
        if not hasattr(field,'column'):
            raise BaseException(_("Django's independent fields must use the ApiResponseModelFields class"))
        return {
            'name':field.column,
            'type':type(field).__name__,
            'desc':field.verbose_name,
        }
    def __mk_flask_model_field_doc(self,field):
        return {
            'name':field.name,
            'type':str(field.type),
            'desc':field.comment,
        }
    
    def __find_response_docs(self,key,docs_node):
        # 容器层
        children = []
        type_ = ''
        desc = ''
        str_type = str(type(docs_node))
        if type(docs_node) == str:
            # 手写描述规定格式：key:type:desc
            # 比如photos:Array:照片url字符串组成的列表数据
            arr = docs_node.split(':')
            if len(arr)==3:
                key = arr[0]
                type_ = arr[1]
                desc= arr[2]
            else:
                desc = docs_node
        elif type(docs_node) == dict:
            # 字典容器递归
            type_='Object'
            for k,v in docs_node.items():
                this = self.__find_response_docs(k,v)
                if type(this) == list:
                    children += this
                elif type(this) == dict:
                    children.append(this)
        elif type(docs_node) == set:
            # 集合，用来表示单个对象
            type_='Object'
            for v in docs_node:
                this = self.__find_response_docs(key,v)
                if type(this) == list:
                    children += this
                elif type(this) == dict:
                    children.append(this)
        elif type(docs_node) == list:
            # 列表对象,包含可能多组字段
            type_='Array'
            for v in docs_node:
                this = self.__find_response_docs(key,v)
                if type(this) == list:
                    children += this
                elif type(this) == dict:
                    children.append(this)
        elif 'django.db.models' in str_type:
            if hasattr(docs_node,'_meta'):
                for obj in docs_node._meta.fields:
                    children.append(self.__mk_django_model_field_doc(obj))
            else:
                # 单独django字段
                children.append(self.__mk_django_model_field_doc(docs_node))
            return children
        elif 'ApiResponseModelFields' in str_type:
            # 解析部分字段
            fields = docs_node.get_fields()
            this = self.__find_response_docs(key,fields)
            return this['children']
        elif 'sqlalchemy.sql.schema.Column' in str_type or 'sqlalchemy.orm.attributes' in str_type:
            # flask 单独字段
            return self.__mk_flask_model_field_doc(docs_node)
        elif 'sqlalchemy.orm' in str_type:
            # flask的models
            if hasattr(docs_node, '__table__'):
                for obj in docs_node.__table__._columns:
                    children.append(self.__mk_flask_model_field_doc(obj))
        return {
            'name':key,
            'type':type_,
            'desc':desc,
            'children':children
        }

    def __not_find_url_function(self, request):
        # 如果找不到业务模块
        return return_response(_('no such interface'))

    def __find_api_function(self, url):
        # 查找api所指向的模块
        if (type(url) == tuple and len(url) > 0):
            url = url[0]
        key, value_dict = self.__find_url_rule(url)
        model = self.url_dict.get(key)
        if model:
            return model,key,value_dict
        return self.__not_find_url_function,None,None

    def __find_api_methons(self, url):
        # 查找api所指向的方法
        return self.url_methods.get(url)

    def __find_url_rule(self, url):
        # 从规则列表中匹配当前访问的url
        value_dict = {}
        for obj in self.rule_maps:
            url_ = url
            line = obj['line']
            key = obj['key']
            for rule in line:
                m = re.match(rule['regex'], url_)
                if not m:
                    break
                pos,end = m.span()
                url_ = url_[end:] # 截断url
                if rule['type']=='variable':
                    # 动态查找
                    value_dict.update({
                        rule['variable']: m.group(0)  # {'value':'test'}
                    })
            if url_:
                # 有剩余url，表示该行不匹配
                continue
            else:
                return key, value_dict
        return None,None

    def __init_url_rules(self):
        # _converter_args_re = re.compile(r'''
        #     ((?P<name>\w+)\s*=\s*)?
        #     (?P<value>
        #         True|False|
        #         \d+.\d+|
        #         \d+.|
        #         \d+|
        #         [\w\d_.]+|
        #         [urUR]?(?P<stringval>"[^"]*?"|'[^']*')
        #     )\s*,
        # ''' , re.VERBOSE | re.UNICODE)
        _converter_args_re = re.compile(r'''
        (?P<value>
            (\w+)
        )''' ,re.VERBOSE | re.UNICODE)

        self.rule_maps = [] # 规则映射表
        for rule in self.url_dict.keys():
            index = 0
            this_rule = []
            for converter, arguments, variable in parse_rule(rule):
                if converter is None:
                    # 静态地址
                    this_rule.append({
                        'regex': re.escape(variable),
                        'type':'static'
                        })
                else:
                    # 动态查询
                    this_rule.append({
                        'regex': _converter_args_re,
                        'variable':variable,
                        'converter':converter,
                        'type':'variable'
                        })
                index = index + 1
            self.rule_maps.append({
                'line': this_rule,
                'key':rule
            })
    
    def get_parameter(self, request):
        # 获取参数
        data = {}
        # 获取django的request数据
        if api.framework.name =='django':
            if request.GET:
                for k,v in request.GET.items():
                    if k.endswith('[]'):
                        # 从get传递过来的同名参数，需要重组成list对象
                        v = request.GET.getlist(k)
                        k = k[:-2]
                    data.update({k:v})
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
        if api.framework.name == 'flask':
            if request.args:                
                data.update(request.args.to_dict())
            elif request.form:
                data.update(request.form.to_dict())
            else:
                try:
                    # 某些特殊错误的封装，将get,Content-Type: application/json
                    jd = request.get_json()
                    if jd:
                        data.update(jd)
                except:
                    pass
        if api.framework.name == 'bottle':
            if request.GET:                
                data.update(request.GET)
            if request.POST:
                data.update(request.POST)
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
        options = conf.get('options')
        not_converting = False

        # 没有值得情况，包括'',[],()这种，但是要排除0，因为0经常用于标记值
        if not value and value != 0 and not default_ is None:
            # 默认值如果是一个函数，运行它，并不再检查类型转换
            if callable(default_):
                value = default_()
                not_converting = True
            else:
                value = default_

         # 检查必要值
        if required_ == True and not value and value!=0:
            return _('parameter')+' {} '.format(name)+_('is required'), None

        if value == '' and type_ != str:
            # 如果是空字符串，但是要求类型不是字符串，就转换成None
            value = None
            
        # 检查空值，这个时候因为有些空值还处于字符串形态，比如'[]'，所以有可能会被跳过        
        if not value and value != 0:
            if required_:
                return _('parameter')+' {} '.format(name)+_('can not be empty'), None,
            else:
                return None, value
        
            
        # 检查并转换类型
        if not_converting==False and type_ and type(value) != type_:
            try:
                if type_ in [list, dict, set, tuple]:
                    # 容器类，json验证后转换
                    value = type_(json.loads(value))
                elif type_ == bool:
                    if value == 'true':
                        value = True
                    else:
                        value = False
                else:
                    # 其他类型或者类型转换器
                    value = type_(value)
            except:
                return _('parameter')+' {} '.format(name)+_('must be type')+' {} '.format(type_), None

        # 检查转换后的'',[],(),{}都放弃长度检查，0继续检查大小。
        if not value and value != 0:
            if required_:
                return _('parameter')+' {} '.format(name)+_('can not be empty'), None
            else:
                return None, value
        # 检查可选项目
        if options and type(options)==list:
            if value not in options:
                return _('parameter') + ' {} '.format(name) + _('must be in the list of options') + ' : {}'.format(json.dumps(options)), None
                
        # 检查最小值/长度
        if min_:
            if type(value) in [str, list, dict, set]:
                if len(value) < min_:
                    return _('parameter')+' {} '.format(name)+_('minimum length')+' {} '.format(min_), None
            elif type(value) in [int, float, complex]:
                if value < min_:
                    return _('parameter')+' {} '.format(name)+_('minimum value')+' {} '.format(min_), None
            else:
                # 其他自定义类型
                if value < type_(min_):
                    return _('parameter')+' {} '.format(name)+_('minimum value')+' {} '.format(min_), None

        # 检查最大值/长度
        if max_:
            if type(value) in [str, list, dict, set]:
                if len(value) > max_:
                    return _('parameter')+' {} '.format(name)+_('maximum length')+' {} '.format(max_), None
            elif type(value) in [int, float, bool, complex]:
                if value > max_:
                    return _('parameter')+' {} '.format(name)+_('maximum value')+' {} '.format(max_), None
            else:
                # 其他自定义类型
                if value > type_(max_):
                    return _('parameter')+' {} '.format(name)+_('maximum value')+' {} '.format(max_), None
        
        return None, value

    def verify_parameter(self, request, par_conf,value_dict=None,parameter=None):
        # 校验参数合法性，并转换成参数对象
        if type(par_conf) != list:
            return _('The wrong configuration, methons must be loaded inside the list container.'), None
        if parameter is None:
            parameter = self.get_parameter(request)
        if value_dict:
            parameter.update(value_dict)
        adc = ApiDataClass()
        errmsg = []
        # 从参数配置获取参数
        for line in par_conf:
            key = line['name']
            errmsg_, value = self.__verify(line, key, parameter.get(key))
            if errmsg_:
                errmsg.append(errmsg_)
            else:
                setattr(adc, key, value)
        return errmsg, adc

    def api_run(self, request, url, method=None, parameter=None, json=True):
        '''在代码中直接运行接口，方便复用接口代码
        request   直接传入当前request，
        url       就是你想要访问的接口url
        method    如果不传入，就是 = request.method
        parameter 请求参数，如果不传入，就没有参数传入到api中
        json      默认True返回json数据，False就会返回response
        '''
        if not method:
            method = request.method
        model, key, value_dict = self.__find_api_function(url)
        methons = self.__find_api_methons(key)
        errmsg = ''
        if methons and not method is None:
            # 有配置方法和参数，校验参数合法性，并转换参数
            par_conf = methons.get(method.upper())
            if parameter is None:
                parameter = {}
            errmsg, data = self.verify_parameter(None, par_conf,value_dict=value_dict,parameter=parameter)
        else:
            errmsg = _('no such interface method')
        if errmsg:
            if json:
                return {'msg': errmsg}, 400
            return return_response(errmsg)
        ret = model(request, data, json, method)
        return ret

    def api_entry(self,request,*url):
        '''api入口'''
        model, key, value_dict = self.__find_api_function(url)
        methons = self.__find_api_methons(key)
        
        if methons and not methons.get(request.method) is None:
            # 有配置方法和参数，校验参数合法性，并转换参数
            errmsg, data = self.verify_parameter(request, methons.get(request.method),value_dict)
            if errmsg:
                return return_response(errmsg)
        else:
            return return_response(_('no such interface method'))
   
        ret = model(request, data)
        return ret

    def render_documents(self,request,*url):
        '''渲染文档'''
        if self.document_version != time.ctime(os.stat(self.document_name).st_mtime):
            # 如果文档发生变化，读取文档。
            self.document = open(self.document_name, mode='r', encoding='utf-8').read()
        return api.framework.template(self.document)
 
    def get_api_data(self, request, *url):
        '''返回给文档页面数据'''
        return api.framework.json({'data': self.conf,'options':self.options})

        