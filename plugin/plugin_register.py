# -*- coding: utf-8 -*-
# Time    : 2021/1/30 21:45
# Author  : LiaoKong
import os
import pkgutil
from result_item import ResultItem


class ExistedError(Exception):
    pass


class PluginRegister(object):
    def __init__(self):
        self._plugins_storage = {}
        self.keyword_by_shortcut = {}
        self.load_plugins()

    def load_plugins(self):
        for importer, package_name, _ in pkgutil.iter_modules(
                [os.path.join(os.path.dirname(os.path.dirname(__file__)), 'plugins')]):
            module = importer.find_module(package_name).load_module(package_name)
            for cls_str in dir(module):
                class_obj = getattr(module, cls_str)
                if hasattr(class_obj, 'is_plugin'):
                    obj = class_obj()
                    if obj.keyword in self._plugins_storage:
                        raise ExistedError('Keyword {} already exists'.format(obj.keyword))
                    self._plugins_storage[obj.keyword] = obj

        self.init_keyword_by_shortcut()

    def reload_plugins(self):
        self._plugins_storage = {}
        self.keyword_by_shortcut = {}
        self.load_plugins()

    def search_plugin(self, text):
        if not text:
            return []

        return [ResultItem(o.title, o.description, o.keyword, o.icon_path)
                for k, o in sorted(self._plugins_storage.items(), key=lambda x: x[0])
                if text in k]

    def execute(self, keyword, execute_str, plugin_by_keyword):
        return self._plugins_storage[keyword].run(execute_str, plugin_by_keyword)

    def get_plugin(self, keyword):
        return self._plugins_storage.get(keyword)

    def plugins(self):
        return self._plugins_storage

    def init_keyword_by_shortcut(self):
        self.keyword_by_shortcut = {o.shortcut: o.keyword for o in self._plugins_storage.values() if o.shortcut}


if __name__ == '__main__':
    pr = PluginRegister()
