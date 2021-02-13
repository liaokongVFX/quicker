# -*- coding: utf-8 -*-
# Time    : 2021/2/13 21:04
# Author  : LiaoKong
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from utils import get_logger

log = get_logger(u'定时任务')


class TimingTasksManager(QObject):
    show_msg_sig = Signal(str)

    def __init__(self, parent=None):
        super(TimingTasksManager, self).__init__(parent)

        self._jobs_storage = {}

        executors = {
            'default': ThreadPoolExecutor(10),
            'processpool': ProcessPoolExecutor(3)
        }

        self.scheduler = BackgroundScheduler(executors=executors)
        self._load_jobs()
        self.scheduler.start()
        log.info(u'成功启动定时任务')

    def _load_jobs(self):
        # todo 从本地加载上次设置的定时任务
        pass

    def add_job(self, job_type, kwargs):
        msg = kwargs.pop('msg')
        obj = self.scheduler.add_job(lambda: self.show_msg(msg), job_type, **kwargs)
        self._jobs_storage[obj.id] = obj

    def show_msg(self, msg):
        self.show_msg_sig.emit(msg)
