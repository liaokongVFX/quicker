# -*- coding: utf-8 -*-
# Time    : 2021/2/15 17:08
# Author  : LiaoKong
import webbrowser

from core import register
from core.action_base import AbstractAction, TEXT


class WebSearchAction(AbstractAction):
    action_types = [TEXT]

    def run(self, text):
        webbrowser.open(self.url_parse.format(text))


@register
class BaiduSearchAction(WebSearchAction):
    title = u'百度搜索'
    description = u'使用百度搜索所选关键词'
    url_parse = u'https://www.baidu.com/s?ie=UTF-8&wd={}'


@register
class GoogleSearchAction(WebSearchAction):
    title = u'google搜索'
    description = u'使用Google搜索所选关键词'
    url_parse = u'https://www.google.com/search?q={}'
