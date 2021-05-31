#!/usr/bin/env python3

from datetime import datetime as dt
from .api_shop import _
import re
class DataExpansion(type):
  def __repr__(self):
    return self.class_name or "<class 'data_format'>"

class baseFormat(object, metaclass=DataExpansion):
    '''基础格式，方便动态继承'''

class datetime(object, metaclass=DataExpansion):
    '''将str转换成datetime格式'''
    class_name = f"<class '{_('datetime')}'>"
    def __new__(self, value):
        if ':' in value:
            return dt.strptime(value, '%Y-%m-%d %H:%M:%S')
        else:
            return dt.strptime(value, '%Y-%m-%d')
    @staticmethod
    def now():
        return dt.now()

def __regex__(self, value):
    '''用正则校验参数'''
    if self.func == 'search':
        ret = re.search(self.regex, value, self.flag)
    elif self.func == 'match':
        ret = re.match(self.regex, value, self.flag)
    else:
        ValueError(_('regular not have this func.'))
    if ret:
        return value
    raise ValueError(_('regular test failed.'))

class regex(type, metaclass=DataExpansion):
    '''正则校验参数
    regex(reg, func = 'match')
    参数：
        reg = 正则语法
        name = RegularCheck  你要求的参数格式说明
        func = 默认使用match方法校验 ，你可以改成match或者search
        flag = 正则参数
    '''
    class_name = f"<class '{_('regex')}'>"
    def __new__(self, reg, name = 'RegularCheck', func = 'match', flag = 0):
        Hello = type('Hello', (baseFormat,), dict(__new__=__regex__))
        Hello.regex = reg
        Hello.func = func
        Hello.flag = flag
        Hello.class_name = f"<class '{_(name)}'>"
        return Hello


numeric = regex(r'^\d+$', name='numeric')
email = regex(r'^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$', name='email')
chinese = regex(r'^[\u0391-\uFFE5]+$', name='chinese')
url = regex(r'^[a-zA-Z]+://(\w+(-\w+)*)(\.(\w+(-\w+)*))*(\?\s*)?$', name='url')
cellphone = regex(r'^1\d{10}$', name='cellphone')
idcard = regex(r'^([1-9]\d{5}[12]\d{3}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])\d{3}[0-9xX])$', name='idcard')



