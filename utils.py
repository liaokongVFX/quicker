# -*- coding: utf-8 -*-
# Time    : 2021/2/8 18:38
# Author  : LiaoKong
import sys
import logging
from logging.handlers import TimedRotatingFileHandler

from ctypes import windll
from setting import RECORD_LOG


class SingleLogger(object):
    log = logging.getLogger('Beefalo')
    log.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(plugin_name)s - %(levelname)s - %(message)s')
    log_file_handler = TimedRotatingFileHandler(filename='./log/Quicker.log', when='D', encoding='utf-8')
    log_file_handler.setFormatter(formatter)
    log_file_handler.setLevel(logging.INFO)
    log.addHandler(log_file_handler)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)

    def __init__(self, name='Beefalo'):
        self.name = name

    def add_name_info(self, kwargs):
        if not kwargs:
            kwargs = {}
        if 'extra' not in kwargs:
            kwargs['extra'] = {}
        kwargs['extra']['plugin_name'] = self.name
        return kwargs

    def info(self, msg, *args, **kwargs):
        kwargs = self.add_name_info(kwargs)
        print(kwargs)
        self.log.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        kwargs = self.add_name_info(kwargs)
        self.log.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        kwargs = self.add_name_info(kwargs)
        self.log.error(msg, *args, **kwargs)


def get_logger(name):
    if RECORD_LOG:
        return SingleLogger(name)


def clear_clipboard():
    if windll.user32.OpenClipboard(None):
        windll.user32.EmptyClipboard()
        windll.user32.CloseClipboard()
