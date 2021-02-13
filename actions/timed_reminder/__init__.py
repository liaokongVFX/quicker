# -*- coding: utf-8 -*-
# Time    : 2021/2/13 21:23
# Author  : LiaoKong

from core import register
from core.action_base import AbstractAction, EMPTY, TEXT
import notification


@register
class TimedReminder(AbstractAction):
    title = u'定时提醒'
    description = u'设置定时提醒'
    action_types = [EMPTY, TEXT]

    def run(self, data):
        # todo 添加定时设置界面
        self.main_window.timing_task_manager.add_job('interval', {'seconds': 6, 'msg': '666666'})

