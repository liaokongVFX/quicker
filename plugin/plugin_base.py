# -*- coding: utf-8 -*-
# Time    : 2021/1/30 21:23
# Author  : LiaoKong
from functools import wraps


def register_plugin(obj):
    obj.is_plugin = True
    @wraps(obj)
    def inner(*args, **kwargs):
        class_obj = obj(*args, **kwargs)
        return class_obj

    return inner


class AbstractPlugin(object):
    title = ''
    keyword = ''
    icon = ''
    description = ''

    def query(self, text):
        raise NotImplementedError
