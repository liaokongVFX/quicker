# -*- coding: utf-8 -*-
# Time    : 2021/2/15 17:34
# Author  : LiaoKong
from core import register
from core.action_base import AbstractAction, TEXT
from widget import TranslationWidget
from translation import translation


@register
class TranslationAction(AbstractAction):
    title = u'划词翻译'
    description = u'划词翻译'
    action_types = [TEXT]

    def run(self, text):
        dst = '\n\n'.join(translation(text))
        tw = TranslationWidget(text, dst)
        tw.show_window()
        tw.exec_()
