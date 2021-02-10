# -*- coding: utf-8 -*-
# Time    : 2021/1/30 21:23
# Author  : LiaoKong
import core


class AbstractPlugin(core.AbstractBase):
    title = ''
    keyword = ''
    icon = ''
    description = ''
    shortcut = ''

    main_window = None  # 这个值不需要初始化，在插件加载时，会自动设置为全局Quicker对象
    _verify_fields = ['title', 'keyword', 'description']

    def run(self, text, plugin_by_keyword):
        raise NotImplementedError

    def query(self, text):
        pass
