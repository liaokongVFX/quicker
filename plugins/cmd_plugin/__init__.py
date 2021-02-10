# -*- coding: utf-8 -*-
# Time    : 2021/1/31 19:44
# Author  : LiaoKong
import os

from core import register
from core.plugin_base import AbstractPlugin


@register
class CmdPlugin(AbstractPlugin):
    title = u'CMD'
    keyword = 'cmd'
    description = u'执行CMD命令'

    def run(self, text, plugin_by_keyword):
        os.system('start cmd /k {}'.format(text))


if __name__ == '__main__':
    cp = CmdPlugin()
    cp.run('ipconfig')
