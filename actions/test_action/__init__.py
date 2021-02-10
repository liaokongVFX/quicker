# -*- coding: utf-8 -*-
# Time    : 2021/2/10 17:02
# Author  : LiaoKong

from core import register
from core.action_base import AbstractAction, EMPTY, FILE, MULT_FILES


@register
class TestAction(AbstractAction):
    title = 'test'
    description = u'这是一个测试的action'
    action_types = [FILE, MULT_FILES]

    def run(self, data):
        print '6' * 66
        print data
        print '6' * 66
