#!/usr/bin/env python3

from datetime import datetime as dt

class datetime():
    '''将str转换成datetime格式'''

    def __new__(self, string):
        if ':' in string:
            return dt.strptime(string, '%Y-%m-%d %H:%M:%S')
        else:
            return dt.strptime(string, '%Y-%m-%d')
