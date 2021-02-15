# -*- coding: utf-8 -*-
# Time    : 2021/2/15 20:49
# Author  : LiaoKong

from core import register
from core.action_base import AbstractAction, EMPTY
from widget import PickColorWidget


@register
class PickColor(AbstractAction):
    title = u'拾取颜色'
    description = u'按P键拾取鼠标所在位置的颜色'
    action_types = [EMPTY]

    def run(self, _):
        pcw = PickColorWidget()
        pcw.show()
