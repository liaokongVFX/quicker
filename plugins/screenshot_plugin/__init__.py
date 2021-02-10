# -*- coding: utf-8 -*-
# Time    : 2021/2/9 17:30
# Author  : LiaoKong
import os
import subprocess
from PySide2.QtWidgets import QApplication, QFileDialog

from core.plugin_base import register_plugin, AbstractPlugin


@register_plugin
class ScreenshotPlugin(AbstractPlugin):
    title = u'截图'
    keyword = 'scr'
    description = u'截图功能，只输入scr会截图到剪切板，如果输入scr s可以保存截图'

    def run(self, text, plugin_by_keyword):
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
        else:
            startupinfo = None
        self.main_window.set_visible()
        grab = subprocess.Popen('rundll32.exe {}/PrScrn.dll PrScrn'.format(
            os.path.dirname(__file__)), startupinfo=startupinfo)
        grab.wait()
        if text:
            clipboard = QApplication.clipboard()
            data_image = clipboard.pixmap()
            if data_image:
                file_path, _ = QFileDialog.getSaveFileName(
                    None, u'请选择截图保存的位置', u'C:/未命名.png', "Images (*.png *.jpg)")
                if file_path:
                    data_image.save(file_path.replace('\\', '/'))
