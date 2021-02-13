# -*- coding: utf-8 -*-
# Time    : 2021/1/24 17:53
# Author  : LiaoKong
import sys
import ctypes
from functools import partial

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from quicker import Quicker
from utils import get_logger
import setting

log = get_logger(u'托盘')


def add_action(menu, name, connect_func, parent, icon=None):
    if icon:
        action = QAction(QIcon(icon), name, parent)
    else:
        action = QAction(name, parent)
    action.triggered.connect(connect_func)
    menu.addAction(action)
    return action


def tray_clicked(tray, quicker, reason):
    if reason is tray.Trigger:
        quicker.set_visible()


if __name__ == '__main__':
    log.info(u'=========启动Quicker=============')
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setWindowIcon(QIcon('res/launch.png'))

    # 属性任务栏图标
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('quicker')

    tray = QSystemTrayIcon()
    quicker = Quicker()

    tray.setIcon(QIcon('res/launch.png'))
    menu = QMenu()
    tray.setContextMenu(menu)

    add_action(menu, u'主界面', quicker.set_visible, app)
    if setting.DEBUG:
        add_action(menu, u'重载插件', quicker.reload_plugin, app)
        add_action(menu, u'重载actions', quicker.reload_actions, app)
    add_action(menu, u'退出', app.exit, app)
    # todo 添加定时提醒编辑和删除菜单

    tray.activated.connect(partial(tray_clicked, tray, quicker))

    tray.show()

    sys.exit(app.exec_())
