# -*- coding: utf-8 -*-
# Time    : 2021/2/13 21:04
# Author  : LiaoKong
import codecs
import json
from datetime import datetime

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
        executors = {
            'default': ThreadPoolExecutor(10),
            'processpool': ProcessPoolExecutor(3)
        }

        self.scheduler = BackgroundScheduler(executors=executors)
        self._load_jobs()
        self.scheduler.start()
        log.info(u'成功启动定时任务')

    def _load_jobs(self):
        # 从本地加载上次设置的定时任务
        with codecs.open('timing_tasks.json', encoding='utf8') as f:
            tasks_data = json.loads(f.read())
        with codecs.open('timing_tasks.json', 'w', encoding='utf8') as f:
            f.write(json.dumps({}, ensure_ascii=False, indent=4))

        for data in tasks_data.values():
            job_type = data.pop('trigger')

            # 过期的只执行一次的定时提醒就不再保存了
            if job_type == 'date' and datetime.strptime(data['run_date'], '%Y-%m-%d %H:%M:%S') < datetime.now():
                continue

            self.add_remind(job_type, data)

    def get_remind_by_id(self):
        jobs = self.scheduler.get_jobs()
        with codecs.open('timing_tasks.json', encoding='utf8') as f:
            tasks_data = json.loads(f.read())
        remind_by_id = {}
        for job in jobs:
            remind_by_id[job.id] = tasks_data.get(job.id, {}).get('msg', '')

        return remind_by_id

    def add_remind(self, job_type, kwargs):
        data = {'data': dict(**kwargs)}
        data['data'].update({'trigger': job_type})

        msg = kwargs.pop('msg')
        obj = self.scheduler.add_job(lambda: self.show_msg(msg), job_type, **kwargs)

        data.update({'id': obj.id})
        self.update_json(data)
        log.info(u'添加定时提醒')
        log.info(data)

    def remove_remind(self, ids):
        for remind_id in ids:
            self.scheduler.remove_job(remind_id)
            self.update_json({'id': remind_id}, True)
            log.info(u'删除定时提醒')

    @staticmethod
    def update_json(data, remove=False):
        with codecs.open('timing_tasks.json', encoding='utf8') as f:
            tasks_data = json.loads(f.read())
            if remove:
                tasks_data.pop(data['id'])
            else:
                tasks_data[data['id']] = data['data']

        with codecs.open('timing_tasks.json', 'w', encoding='utf8') as f:
            f.write(json.dumps(tasks_data, ensure_ascii=False, indent=4))

    def show_msg(self, msg):
        self.show_msg_sig.emit(msg)
