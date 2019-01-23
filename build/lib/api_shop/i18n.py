#!/usr/bin/env python3

class i18n_init():
    '''多国语言模块
    '''
    lang = {
        'en': {
            'django version error': 'Django version is not compatible',
            'not flask or django': 'Currently only compatible with django and flask',
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
        },
        'zh': {
            'django version error': 'Django 版本不兼容，推荐升级到2.x',
            'not flask or django': '目前只支持Flask和Django',
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
            'no such interface method': '没有这个接口method',

        }
    }

    def __init__(self, lang_name):
        self.lang_name = lang_name

    def _(self, text):
        cur = self.lang.get(self.lang_name)
        if not cur:
            return text
        return cur.get(text) or text
