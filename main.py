# -*- coding: utf-8 -*-
# Time    : 2021/1/24 17:53
# Author  : LiaoKong
import sys

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from result_item import ResultItem


class Quicker(QDialog):
    def __init__(self, parent=None):
        super(Quicker, self).__init__(parent)

        self.placeholder = u'请输入关键字'
        self.focus_out_close = True

        pos = QDesktopWidget().availableGeometry().center()
        pos.setX(pos.x() - (self.width() / 2) - 150)
        pos.setY(pos.y() - 350)
        self.move(pos)

        self.init_ui()

        self.add_item(u'百度搜索', u'快速进行百度搜索')
        self.add_item(u'google搜索', u'快速进行google搜索')

        self.input_line_edit.setFocus(Qt.MouseFocusReason)

    def init_ui(self):
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.setFixedSize(QSize(850, 300))

        self.load_style()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self.input_line_edit = QLineEdit()
        self.input_line_edit.setPlaceholderText(self.placeholder)
        self.input_line_edit.setFocusPolicy(Qt.ClickFocus)
        self.input_line_edit.setMinimumHeight(66)
        self.input_line_edit.focusOutEvent = self.focus_out_event
        self.input_line_edit.returnPressed.connect(self.input_line_edit_return_pressed)

        # todo list高度需要根据数据个数自动调整
        self.result_list_widget = QListWidget()
        self.result_list_widget.setObjectName('result_list_widget')
        self.result_list_widget.setFocusPolicy(Qt.ClickFocus)
        self.result_list_widget.focusOutEvent = self.focus_out_event

        layout.addWidget(self.input_line_edit)
        layout.addWidget(self.result_list_widget)

    def input_line_edit_return_pressed(self):
        text = self.input_line_edit.text().strip()
        print text

    def focus_out_event(self, event):
        # 如果当前没有focus的widget就关闭
        widget = QApplication.focusWidget()
        if not widget and self.focus_out_close:
            self.close()

    def load_style(self):
        with open('res/theme.css') as f:
            self.setStyleSheet(f.read())

    def show(self):
        self.input_line_edit.setText('')
        super(Quicker, self).show()

    def reload_plugin(self):
        pass

    def add_item(self, title, description, icon='', date_time='', checkbox=None):
        item = QListWidgetItem()
        item.setSizeHint(QSize(200, 66))
        result_item = ResultItem(title, description, icon, date_time, checkbox)
        self.result_list_widget.addItem(item)
        self.result_list_widget.setItemWidget(item, result_item)


def add_action(menu, name, connect_func, parent, icon=None, shortcut=''):
    if icon:
        action = QAction(QIcon(icon), name, parent)
    else:
        action = QAction(name, parent)
    action.setShortcut(shortcut)
    action.triggered.connect(connect_func)
    menu.addAction(action)
    return action


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    tray = QSystemTrayIcon()
    quicker = Quicker()

    tray.setIcon(QIcon('res/launch.png'))
    menu = QMenu()
    tray.setContextMenu(menu)

    add_action(menu, u'主界面', quicker.show, app, shortcut='ctrl+`')
    add_action(menu, u'重载插件', quicker.reload_plugin, app)
    add_action(menu, u'退出', app.exit, app)

    tray.show()

    sys.exit(app.exec_())
