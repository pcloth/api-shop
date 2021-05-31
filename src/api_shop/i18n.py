#!/usr/bin/env python3

class i18n_init():
    '''多国语言模块
    '''
    lang = {
        'en': {
            'no attributes found': 'No attributes found: ',
            'not found in conf': 'Not found in conf: ',
            'document template not found': 'Document template not found',
            'no such interface': 'No such interface',
            'is required': 'is required',
            'parameter': 'Parameter',
            'can not be empty': 'can not be empty',
            'must be type': 'must be type',
            'minimum length': 'minimum length',
            'minimum value': 'minimum value',
            'maximum length': 'maximum length',
            'maximum value': 'maximum value',
            'The wrong configuration, methons must be loaded inside the list container.': 'The wrong configuration, methons must be loaded inside the list container.',
            'no such interface method': 'No such interface method',
            'Framework version is not compatible.': 'Framework version is not compatible.',
            'Not support': 'Not support',
            'supported framework as follows:': 'supported framework as follows:',
            'Did not find the framework': 'Did not find the framework. Please install ',
            'must be in the list of options': 'must be in the list of options',
            'value is not string type number.':'value is not string type number.',
        },
        'zh': {
            'no attributes found': '没有找到属性：',
            'not found in conf': '在conf参数中没找到方法: ',
            'no such interface': '没有这个接口',
            'is required': '是必要的',
            'parameter': '参数',
            'can not be empty': '不能为空',
            'must be type': '必须是类型',
            'minimum length': '最小长度',
            'minimum value': '最小值',
            'maximum length': '最大长度',
            'maximum value': '最大值',
            'The wrong configuration, methons must be loaded inside the list container.': '错误的配置，methons必须装的list容器内。',
            'no such interface method': '这个接口没有这个method',
            'Framework version is not compatible.': 'api-shop不支持当前框架版本。',
            'Not support': '不支持',
            'supported framework as follows:': '支持的框架如下：',
            'Did not find the framework': '没找指定的框架，请安装',
            'must be in the list of options': '必须在可选项列表中',
            'request.method and method are not equal': 'request.method和method不相等',
            'api-shop return result is not success.': 'api-shop返回结果不成功。',
            'value is not string type number.': '值不是字符串数字。',
            'numeric': '字符串数字',
            'email': '邮箱',
            'chinese': '中文',
            'cellphone': '手机号',
            'idcard':'身份证',
            "Django's independent fields must use the ApiResponseModelFields class":'django的独立字段必须使用ApiResponseModelFields类',
            "Please use the ApiShop.api_run instance method instead of this method, this method will be removed in later versions!!":"请使用ApiShop.api_run实例方法替代本方法，后期版本将移除本方法!!",
        }
    }

    def __init__(self, lang_name):
        self.lang_name = lang_name

    def _(self, text):
        cur = self.lang.get(self.lang_name)
        if not cur:
            return text
        return cur.get(text) or text
