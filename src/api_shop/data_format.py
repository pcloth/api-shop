#!/usr/bin/env python3

from datetime import datetime as dt

class DataExpansion(type):
  def __repr__(self):
    return self.class_name or "<class 'data_format'>"

class datetime(object,metaclass=DataExpansion):
    '''将str转换成datetime格式'''
    
    class_name = "<class 'data_format.datetime'>"

    def __new__(self, string):
        if ':' in string:
            return dt.strptime(string, '%Y-%m-%d %H:%M:%S')
        else:
            return dt.strptime(string, '%Y-%m-%d')
    @staticmethod
    def now():
        return dt.now()
