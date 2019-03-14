#!/usr/bin/env python3

'''
api 工厂
可以让用户用数据来配置api模块，并自动校验参数合法性和生成文档页面。
by pcloth
'''
import json, traceback, os, re, time

from .i18n import i18n_init
from .__init__ import __version__
from .url_parse import parse_rule
from .autofill import auto_fill,check_fill_methods

i18 = i18n_init('zh')

_ = i18._


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
            raise _('django version error')
if not framework:
    try:
        from flask import render_template_string,jsonify
        framework = 'flask'
    except:
        raise _('not flask or django')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BAD_REQUEST = True

class Namespace(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(_('no attributes found')+'{}'.format(name))

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
        raise _('not flask or django')
    else:
        if framework == 'django':
            return JsonResponse({'status': status_code, 'message': msg})
        if framework == 'flask':
            return jsonify({'msg':msg}),status_code
        raise _('not flask or django') 

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
            if type(retdata)==tuple:
                ret = retdata[0]
                status_code = retdata[1] or 200
            else:
                ret = retdata
            
            # 允许返回空body
            if ret == None:
                ret = ''
            if type(ret)==dict:
                if framework == 'django':
                    return JsonResponse(ret, status=status_code)
                if framework == 'flask':
                    return jsonify(ret), status_code
            else:
                if framework == 'django':
                    return HttpResponse(ret, status=status_code)
                if framework == 'flask':
                    return ret, status_code
            raise _('not flask or django')
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

        if not framework:
            raise _('not flask or django')

        self.options = {
                'version':__version__,
                'base_url':'/api/', # 基础url，用以组合给前端的api url
                'bad_request': True,  # 参数bad_request如果是真，发生错误返回一个坏请求给前端，否则都返回200的response，里面附带status=error和msg附带错误信息
                'document': BASE_DIR + '/api_shop/static/document.html',  # 文档路由渲染的模板
                'lang': 'en',
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

        # 扩展语言包
        if type(self.options.get('lang_pack'))==dict:
            self.i18n.lang.update(self.options.get('lang_pack'))
        
        # 切换语言
        self.i18n.lang_name = self.options.get('lang')


        global BAD_REQUEST
        BAD_REQUEST = self.options.get('bad_request',True)

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
            mod = __import__(path)
            for comp in components[1:]:
                mod = getattr(mod,comp)
            return mod
        except:
            try:
                exec('from {} import {}'.format(path, components[-1]))
                return eval(components[-1])
            except:
                # 无法加载
                if auto_fill(thisconf, self.options) == True:
                    # 自动生成文件或者方法，成功后重试一次。
                    return self.__dynamic_import(thisconf)
            

    def __make_model(self, conf):
        # 将字符串里的function模块和函数加载进来，并写入到run_function字段方便调用。
        for i in range(len(conf)):
            # model = dynamic_import(conf[i]['class'])
            model = self.__dynamic_import(conf[i])
            if type(conf[i]['class'])!=str:
                # 直接使用对象
                conf[i]['class'] = self.__class_to_json(conf[i]['class'])
            self.url_dict.update({
                conf[i]['url']: model,
            })
            self.url_methods.update({
                conf[i]['url']: conf[i]['methods'],
            })
            conf[i]['methods'] = self.__class_to_json(conf[i]['methods'])
            
            if hasattr(model,'__doc__'):
                conf[i]['document'] = getattr(model, '__doc__')
            conf[i]['methods_documents'] = {}
            if self.options.get('auto_create_method'):
                check_fill_methods(model,conf[i])
            for key in ['get', 'post', 'delete', 'put', 'patch']:
                # 把业务类子方法的文档添加到数据表
                if hasattr(model, key):
                    mt = getattr(model, key)
                    if hasattr(mt, '__doc__'):
                        conf[i]['methods_documents'].update({key.upper(): getattr(mt, '__doc__')})


        return conf

    def __not_find_url_function(self, request):
        # 如果找不到业务模块
        return return_response(_('no such interface'),400)


    def __find_api_function(self, url):
        # 查找api所指向的模块
        if (type(url) == tuple and len(url) > 0):
            key, value_dict = self.__find_url_rule(url[0])
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
        if framework == 'flask':
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
        return data

        
    def __verify(self, conf, name, value):
        # 校验数据并转换格式
        required_ = conf.get('required')
        type_ = conf.get('type')
        min_ = conf.get('min')
        max_ = conf.get('max')
        default_ = conf.get('default')
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
                return _('parameter')+' {} '.format(name)+_('can not be empty'), None,
            else:
                return None, value
            
        # 检查最小值/长度
        if min_:
            if type_ in [str, list, dict, set]:
                if len(value) < min_:
                    return _('parameter')+' {} '.format(name)+_('minimum length')+' {} '.format(min_), None
            elif type_ in [int, float, complex]:
                if value < min_:
                    return _('parameter')+' {} '.format(name)+_('minimum value')+' {} '.format(min_), None
            else:
                # 其他自定义类型
                if value < type_(min_):
                    return _('parameter')+' {} '.format(name)+_('minimum value')+' {} '.format(min_), None

        # 检查最大值/长度
        if max_:
            if type_ in [str, list, dict, set]:
                if len(value) > max_:
                    return _('parameter')+' {} '.format(name)+_('maximum length')+' {} '.format(max_), None
            elif type_ in [int, float, bool, complex]:
                if value > max_:
                    return _('parameter')+' {} '.format(name)+_('maximum value')+' {} '.format(max_), None
            else:
                # 其他自定义类型
                if value > type_(max_):
                    return _('parameter')+' {} '.format(name)+_('maximum value')+' {} '.format(max_), None
        
        return None, value

    def verify_parameter(self, request, par_conf,value_dict=None):
        # 校验参数合法性，并转换成参数对象
        if type(par_conf) != list:
            return _('The wrong configuration, methons must be loaded inside the list container.'), None

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
            self.document = open(self.document_name,mode='r',encoding='utf-8').read()
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