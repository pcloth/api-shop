import json, decimal
from datetime import datetime, date

def loads(model_obj, data_dict):
    '''将dict数据按key写入到模具的属性'''
    for key, value in data_dict.items():
        if hasattr(model_obj, key) and getattr(model_obj, key) == value:
            # 数据相同不处理
            continue
        # 更新数据
        setattr(model_obj, key, value)

def __to_dict__(model_obj, exclude=None, include=None, tojson=False, func=False):
    '''将当前数据表转换成dict格式
    # 不将列表中字段转出来
    exclude = ['_sa_instance_state', 'password_hash', '_state', 'password'] 
    # 只将列表中的字段转出来，如果有这个参数时，例外参数失效，
    # 并且默认例外参数不也失效（除非指定了password才会被转出）
    include = [''] 
    '''
    default_exclude = ['_sa_instance_state', 'password_hash', '_state', 'password']
    
    if exclude:
        default_exclude += exclude
    if not include:
        include = []
    out_dict = {}
    dkeys = []
    obj_dict_keys = model_obj.__dict__.keys()
    for key in dir(model_obj):
        if include:
            if key in include:
                dkeys.append(key)
        elif key in default_exclude:
            continue
        elif key in obj_dict_keys:
            dkeys.append(key)
        elif func and type(getattr(model_obj.__class__, key)) == property:
            # 如果是@property属性方法，也提取数据
            dkeys.append(key)
    for key in dkeys:
        value = getattr(model_obj, key)
        if tojson:
            # 转换到json格式
            if isinstance(value, datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(value, date):
                value = value.strftime('%Y-%m-%d')
            elif isinstance(value, decimal.Decimal):
                value = float(value)
        out_dict.update({key: value})
    return out_dict
    
def dumps(model_obj, exclude=None, include=None, string=False, func=True):
        '''
        @model_obj 数据模具

        @exclude 不处理列表中的字段

            默认值 exclude = ['_sa_instance_state', 'password_hash', '_state', 'password'] 
            默认不处理输出密码字段

        @include 只输出列表中的字段

        @string 直接转换成string格式

        @func 默认输出模具类中的属性方法
        '''
        data = __to_dict__(model_obj, exclude=exclude, include=include,tojson=True, func=func)
        if string:
            return json.dumps(data)
        return data

def models_to_list(models, exclude=None, include=None, string=False, func=True):
    ret = []
    for model_obj in models:
        this = dumps(model_obj, exclude=exclude, include=include, string=string, func=func)
        ret.append(this)
    return ret