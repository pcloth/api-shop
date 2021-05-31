import os, re

def __find_path(name):
    # 深度切分：
    deep = name.split('.')
    if len(deep)>=3:
        path = '/'.join(deep[:-1]) # 检查路径
        folder = '/'.join(deep[:-2]) # 第三个开始是文件夹
        filename = deep[-2] # 倒数第二个是文件名
        classname = deep[-1] # 最后一个是类
    elif len(deep)==2:
        path = deep[0]
        folder = None
        filename = deep[0] # 倒数第二个是文件名
        classname = deep[1]  # 最后一个是类
    else:
        # 太短了，不创建文件
        return None, None, None, None
    return path, folder, filename, classname

def auto_fill(thisconf, options):
    name = thisconf['class']

    if type(name)!=str:
        # 直接传入的对象
        return False
    methods = thisconf['methods']

    folder_flag = options.get('auto_create_folder')
    file_flag = options.get('auto_create_file')
    class_flag = options.get('auto_create_class')
    method_flag = options.get('auto_create_method')

    path, folder, filename, classname = __find_path(name)
    if not path:
        return False

    if folder_flag and (not os.path.exists(folder)):
        # 文件夹不存在，
        os.makedirs(folder)

    if file_flag and (not os.path.exists(path+'.py')):
        # 文件不存在
        create_file(path)

    try:
        exec('from {} import {}'.format('.'.join(path), classname))
    except:
        # 类不存在
        if class_flag:
            create_class(path, classname, thisconf)
        else:
            return False
    
    return False

# 将参数填充进文档注释
def fill_method_args(method_):
    string = ''
    for d in method_:
        string += '\n        data.{} # {}'.format(d.get('name'),d.get('description',''))
    return string

# 检查并填充方法和参数备注
def check_fill_methods(model, thisconf):
    name = thisconf['class']
    if type(name)!=str:
        # 直接传入的对象
        return False
    methods = thisconf['methods']
    addstring = ''
    
    for m in methods.keys():
        key = m.lower()
        if not hasattr(model, key):
            # 没有指定方法
            addstring += '''
    def {}(self, request, data):
        """ todo:
        api-shop automatically inserts code{}
        """
        pass'''.format(key,fill_method_args(methods[m]))
    if not addstring:
        return False

    path, folder, filename, classname = __find_path(name)
    if not path:
        return False

    file = open(path + '.py', 'r', encoding='utf-8')
    content = file.read()
    file.close()
    pos = content.find("class {}(".format(classname))
    if pos < 0:
        # 没找到类
        return False

    q = re.compile(r'(\n\S)', re.DOTALL)
    regex_ret = q.search(content[pos:])
    # 如果是换行符后的非空字符，就在前面插入；否则就在文档最后插入
    pos = regex_ret.span()[0] + pos if regex_ret else len(content) - 1
    content = content[:pos] + addstring + content[pos:]
    file = open(path + '.py', 'w', encoding='utf-8')
    file.write(content)
    file.close()

# 创建文件
def create_file(path):
    file = open(path + '.py', 'a',encoding='utf-8')
    file.write('''
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# api-shop automatically inserts code

from api_shop import Api

''')
    file.close()


# 创建类
def create_class(path, classname,thisconf):
    name = thisconf['name']
    methods = thisconf['methods']
    exe_path = '.'.join(thisconf['class'].split('.')[:-1])
    try:
        exec('from {} import Api'.format(exe_path))
    except:
        # print('Api未引入')
        file = open(path + '.py', 'r', encoding='utf-8')
        content = file.read()
        file.close()
        file = open(path + '.py', 'w', encoding='utf-8')
        file.write('# api-shop automatically inserts code\nfrom api_shop import Api\n\n' + content)
        file.close()
    file = open(path + '.py', 'a', encoding='utf-8')
    file.write('''
class {}(Api):
    """{}"""
    pass
''' .format(classname, name))
    file.close()
