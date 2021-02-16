# -*- coding: utf-8 -*-
# Time    : 2021/1/30 21:23
# Author  : LiaoKong
import webbrowser

from core import register
from core.plugin_base import AbstractPlugin


class WebSearchPlugin(AbstractPlugin):
    url_parse = ''

    def run(self, text, result_item, plugin_by_keyword):
        webbrowser.open(self.url_parse.format(text))


@register
class BaiduSearchPlugin(WebSearchPlugin):
    title = u'百度搜索'
    keyword = 'bd'
    description = u'在百度上搜索关键字'
    url_parse = u'https://www.baidu.com/s?ie=UTF-8&wd={}'


@register
class GoogleSearchPlugin(WebSearchPlugin):
    title = u'Google搜索'
    keyword = 'go'
    description = u'在google上搜索关键字'
    url_parse = u'https://www.google.com/search?q={}'


@register
class GithubSearchPlugin(WebSearchPlugin):
    title = u'Github搜索'
    keyword = 'github'
    description = u'在github上搜搜关键字'
    url_parse = u'https://github.com/search?q={}'


if __name__ == '__main__':
    b = BaiduSearchPlugin()
    b.run('aaa')
    print b.is_plugin
