# -*- coding: utf-8 -*-
# Time    : 2021/1/30 21:23
# Author  : LiaoKong
import os
import inspect
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
    shortcut = ''

    def __init__(self):
        self._verify_required_fields()

    @property
    def icon_path(self):
        if self.icon:
            return os.path.join(os.path.dirname(inspect.getfile(self.__class__)), self.icon)
        return ''

    def _verify_required_fields(self):
        for field in ['title', 'keyword', 'description']:
            if not getattr(self, field):
                raise RequiredFieldsError('The {} field is not set.'.format(field))

    def run(self, text, plugin_by_keyword):
        raise NotImplementedError

    def query(self, text):
        pass
