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


class RequiredFieldsError(Exception):
    pass


class AbstractPlugin(object):
    title = ''
    keyword = ''
    icon = ''
    description = ''

    def __init__(self):
        self._verify_required_fields()

    def _verify_required_fields(self):
        for field in ['title', 'keyword', 'description']:
            if not getattr(self, field):
                raise RequiredFieldsError('The {} field is not set.'.format(field))

    def run(self, text, plugin_by_keyword):
        raise NotImplementedError

    def query(self, text):
        pass
