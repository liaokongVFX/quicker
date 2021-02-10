# -*- coding: utf-8 -*-
# Time    : 2021/2/10 15:31
# Author  : LiaoKong
import core

EMPTY = 0
TEXT = 1
MULT_FILES = 2
FILE = 3


class AbstractAction(core.AbstractBase):
    title = ''
    icon = ''
    description = ''
    action_types = []
    exts = []

    _verify_fields = ['title', 'description', 'action_types']

    def run(self, files):
        raise NotImplementedError
