# -*- coding: utf-8 -*-
# Time    : 2021/1/30 21:45
# Author  : LiaoKong
import os
import pkgutil
from result_item import ResultItem
from utils import get_logger

log = get_logger(u'注册插件')


class PluginRegister(object):
    def __init__(self, main_window):
        self.main_window = main_window
        self._plugins_storage = {}
        self.keyword_by_shortcut = {}
        self.load_plugins()

        self._check_shortcuts()
        log.info(u'插件已加载完成.')
        log.info(self._plugins_storage)

    def load_plugins(self):
        for importer, package_name, _ in pkgutil.iter_modules(
                [os.path.join(os.path.dirname(os.path.dirname(__file__)), 'plugins')]):
            module = importer.find_module(package_name).load_module(package_name)
            for cls_str in dir(module):
                class_obj = getattr(module, cls_str)
                if hasattr(class_obj, 'is_plugin'):
                    obj = class_obj()
                    if obj.keyword in self._plugins_storage:
                        log.error('Keyword {} already exists.'.format(obj.keyword))
                        raise ValueError('Keyword already exists.')
                    obj.main_window = self.main_window
                    self._plugins_storage[obj.keyword] = obj

    def _check_shortcuts(self):
        """检查快捷键是否有重复的"""
        shortcuts = [x for x in self._plugins_storage.values() if x.shortcut]
        if len(shortcuts) != len(set(shortcuts)):
            log.error('There are duplicate shortcuts')
            log.error('shortcuts: {}'.format(shortcuts))
            raise ValueError('There are duplicate shortcuts.')

    def reload_plugins(self):
        self._plugins_storage = {}
        self.keyword_by_shortcut = {}
        self.load_plugins()
        log.info(u'插件已成功重新加载')

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

    def get_keyword_by_shortcut(self):
        return {o.shortcut: o.keyword for o in self._plugins_storage.values() if o.shortcut}


if __name__ == '__main__':
    pr = PluginRegister()
