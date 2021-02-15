# -*- coding: utf-8 -*-
# Time    : 2021/2/13 21:23
# Author  : LiaoKong
from libs import qflat

from core import register
from core.action_base import AbstractAction, EMPTY, TEXT

from add_widget import TimedReminderWidget
from remove_widget import RemoveTimedReminderWidget


@register
class AddTimedReminder(AbstractAction):
    title = u'添加定时提醒'
    description = u'添加定时提醒'
    action_types = [EMPTY, TEXT]

    def run(self, data):
        trw = TimedReminderWidget(data.strip())
        trw.show()
        trw.exec_()
        if trw.data:
            trigger = trw.data.pop('trigger')
            self.main_window.timing_task_manager.add_remind(trigger, trw.data)
            qflat.success(u'定时提醒添加成功')


@register
class RemoveRimedReminder(AbstractAction):
    title = u'删除定时提醒'
    description = u'删除定时提醒'
    action_types = [EMPTY]

    def run(self, data):
        remind_by_id = self.main_window.timing_task_manager.get_remind_by_id()
        rtrw = RemoveTimedReminderWidget(remind_by_id)
        rtrw.show()
        rtrw.exec_()
        if rtrw.remove_ids:
            self.main_window.timing_task_manager.remove_remind(rtrw.remove_ids)
            qflat.success(u'已成功删除{}个定时提醒'.format(len(rtrw.remove_ids)))
