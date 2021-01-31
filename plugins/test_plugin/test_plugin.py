# -*- coding: utf-8 -*-
# Time    : 2021/1/31 15:48
# Author  : LiaoKong

from plugin.plugin_base import AbstractPlugin, register_plugin


@register_plugin
class TestPlugin(AbstractPlugin):
    title = u'测试插件'
    description = u'测试插件内容'
    keyword = u'test'

    def run(self, text, plugin_by_keyword):
        print text


@register_plugin
class TestPlugin1(AbstractPlugin):
    title = u'测试插件'
    description = u'测试插件内容'
    keyword = u'test1'

    def run(self, text, plugin_by_keyword):
        print text
