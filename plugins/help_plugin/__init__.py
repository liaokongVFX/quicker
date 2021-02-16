# -*- coding: utf-8 -*-
# Time    : 2021/1/31 20:27
# Author  : LiaoKong
from result_item import ResultItem
from core import register
from core.plugin_base import AbstractPlugin


@register
class HelpPlugin(AbstractPlugin):
    title = u'帮助'
    keyword = 'help'
    description = u'显示所有已加载的插件'
    close_win = False

    def run(self, text, result_item, plugin_by_keyword):
        return [ResultItem(o.title, o.description, o.keyword, o.icon_path)
                for o in sorted(plugin_by_keyword.values(), key=lambda x: x.keyword)]
