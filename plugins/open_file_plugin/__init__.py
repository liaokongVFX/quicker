# -*- coding: utf-8 -*-
# Time    : 2021/2/9 16:46
# Author  : LiaoKong
import os
from core.plugin_base import AbstractPlugin, register_plugin


@register_plugin
class OpenFilePlugin(AbstractPlugin):
    title = u'打开文件'
    keyword = 'cd'
    description = u'通过路径或者关键字打开文件'
    shortcut = 'alt+Q'

    path_by_name = {
        'code': 'D:/code',
        'work': 'D:/work',
        'py': 'D:/Program Files/JetBrains/PyCharm 2019.3.1/bin/pycharm64.exe',
        'mu': 'E:/Program Files (x86)/Netease/CloudMusic/cloudmusic.exe'
    }

    def run(self, text, plugin_by_keyword):
        file_path = self.path_by_name.get(text)
        if not file_path:
            file_path = text.replace('\\', '/')

        if os.path.exists(file_path):
            os.startfile(file_path)
