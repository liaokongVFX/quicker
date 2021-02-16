# -*- coding: utf-8 -*-
# Time    : 2021/2/16 16:13
# Author  : LiaoKong
import os

from PySide2.QtWidgets import QFileIconProvider
from PySide2.QtCore import QFileInfo

from core import register
from core.plugin_base import AbstractPlugin
from result_item import ResultItem

from everything import Everything


@register
class EverythingPlugin(AbstractPlugin):
    title = u'搜索文件'
    description = u'需要打开everthing才能使用'
    keyword = 'find'

    everything = Everything()

    def run(self, text, result_item, plugin_by_keyword):
        os.startfile(result_item.description)

    def query(self, text):
        paths = self.everything.query(text)
        return [ResultItem(os.path.basename(p), p, icon=self._make_icon(p)) for p in paths]

    @staticmethod
    def _make_icon(file_path):
        icon = ''
        if not file_path.endswith('.lnk'):
            icon = QFileIconProvider().icon(QFileInfo(file_path)).pixmap(50, 50)
        return icon
