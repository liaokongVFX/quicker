# -*- coding: utf-8 -*-
# Time    : 2021/2/13 21:23
# Author  : LiaoKong
from libs import qflat

from core import register
from core.action_base import AbstractAction, EMPTY, TEXT

from mian_widget import TimedReminderWidget


@register
class TimedReminder(AbstractAction):
    title = u'定时提醒'
    description = u'设置定时提醒'
    action_types = [EMPTY, TEXT]

    def run(self, data):
        trw = TimedReminderWidget(data.strip())
        trw.show()
        trw.exec_()
        if trw.data:
            trigger = trw.data.pop('trigger')
            self.main_window.timing_task_manager.add_remind(trigger, trw.data)
            qflat.success(u'定时提醒添加成功')
