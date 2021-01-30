# -*- coding: utf-8 -*-
# Time    : 2021/1/30 21:45
# Author  : LiaoKong
import os
import pkgutil


class PluginRegister(object):
    def __init__(self):
        self._plugins_storage = {}
        self.load_plugins()

    def load_plugins(self):
        for importer, package_name, _ in pkgutil.iter_modules(
                [os.path.join(os.path.dirname(os.path.dirname(__file__)), 'plugins')]):
            module = importer.find_module(package_name).load_module(package_name)
            for cls_str in dir(module):
                class_obj = getattr(module, cls_str)
                if hasattr(class_obj, 'is_plugin'):
                    obj = class_obj()
                    self._plugins_storage[obj.keyword] = obj

    def search_plugin(self,text):
        # todo return [result_item（o.title,o.description,o.icon） for k,o in self._plugins_storage.items() if text in k]
        pass




if __name__ == '__main__':
    pr = PluginRegister()
