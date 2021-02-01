# -*- coding: utf-8 -*-
# Time    : 2021/1/24 17:53
# Author  : LiaoKong
import sys
from functools import partial

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from plugin.plugin_register import PluginRegister


class Quicker(QDialog):
    def __init__(self, parent=None):
        super(Quicker, self).__init__(parent)

        self.placeholder = u'请输入关键字'
        self.focus_out_close = True
        self.RESULT_ITEM_HEIGHT = 62

        pos = QDesktopWidget().availableGeometry().center()
        pos.setX(pos.x() - (self.width() / 2) - 150)
        pos.setY(pos.y() - 350)
        self.move(pos)

        self.init_ui()

        self._plugin_register = PluginRegister()
        self.update_result_list_height(0)

    def init_ui(self):
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.setFixedSize(QSize(850, 600))

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
        self.input_line_edit.textChanged.connect(self.input_line_edit_text_changed)

        self.result_list_widget = QListWidget()
        self.result_list_widget.setObjectName('result_list_widget')
        self.result_list_widget.setFocusPolicy(Qt.ClickFocus)
        self.result_list_widget.focusOutEvent = self.focus_out_event
        self.result_list_widget.keyPressEvent = self.result_list_key_press_event
        self.result_list_widget.itemClicked.connect(self.execute_result_item)

        layout.addWidget(self.input_line_edit)
        layout.addWidget(self.result_list_widget)
        layout.addItem(QSpacerItem(40, 100, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.input_line_edit.setFocus(Qt.MouseFocusReason)

    def input_line_edit_text_changed(self, text):
        if (text.endswith(' ') and
                self.result_list_widget.count() == 1 and
                ' ' not in text.strip() and
                self.result_list_widget.itemWidget(self.result_list_widget.item(0)).keyword != text.strip()):
            self.input_line_edit.setText(
                self.result_list_widget.itemWidget(self.result_list_widget.item(0)).keyword + ' '
            )
            return

        if ' ' not in text.strip():
            plugin_keyword = text.strip()
            result_items = self._plugin_register.search_plugin(plugin_keyword)
            self.add_items(result_items)
        else:
            plugin_keyword, query_str = text.strip().split(' ', 1)

    def update_result_list_height(self, result_items_num):
        # list高度需要根据数据个数自动调整
        height = result_items_num * self.RESULT_ITEM_HEIGHT
        if height > 6 * self.RESULT_ITEM_HEIGHT:
            height = 6 * self.RESULT_ITEM_HEIGHT

        self.result_list_widget.setFixedHeight(height)

    def keyPressEvent(self, event):
        current_widget = QApplication.focusWidget()
        if event.key() == Qt.Key_Down:
            if self.result_list_widget.count() < 1:
                return
            if isinstance(current_widget, QLineEdit):
                self.result_list_widget.setFocus(Qt.MouseFocusReason)
                self.result_list_widget.setCurrentRow(0)
                return
            elif (isinstance(current_widget, QListWidget) and
                  self.result_list_widget.currentRow() + 1 == self.result_list_widget.count()):
                self.input_line_edit.setFocus(Qt.MouseFocusReason)
                self.result_list_widget.setCurrentRow(-1)
                return

        elif event.key() == Qt.Key_Up:
            if isinstance(current_widget, QListWidget):
                self.input_line_edit.setFocus(Qt.MouseFocusReason)
                self.result_list_widget.setCurrentRow(-1)
                return
            elif isinstance(current_widget, QLineEdit) and self.result_list_widget.count():
                self.result_list_widget.setFocus(Qt.MouseFocusReason)
                self.result_list_widget.setCurrentRow(self.result_list_widget.count() - 1)

        return super(Quicker, self).keyPressEvent(event)

    def result_list_key_press_event(self, event):
        if event.key() == Qt.Key_Return:
            return self.execute_result_item(self.result_list_widget.currentItem())

        super(QListWidget, self.result_list_widget).keyPressEvent(event)

    def execute_result_item(self, item):
        result_item = self.result_list_widget.itemWidget(item)
        if result_item.keyword and not self.input_line_edit.text().strip().startswith(result_item.keyword):
            self.input_line_edit.setText(result_item.keyword + ' ')
            self.input_line_edit.setFocus(Qt.MouseFocusReason)
            self.result_list_widget.setCurrentRow(-1)
        else:
            self.input_line_edit_return_pressed()

    def input_line_edit_return_pressed(self):
        if self.result_list_widget.count() != 1:
            # todo 弹出没有关键字的提示
            return

        text = self.input_line_edit.text().strip()
        if len(text.strip().split(' ', 1)) == 2:
            plugin_keyword, execute_str = text.strip().split(' ', 1)
        else:
            plugin_keyword = self.result_list_widget.itemWidget(self.result_list_widget.item(0)).keyword
            execute_str = ''

        result_items = self._plugin_register.execute(plugin_keyword, execute_str, self._plugin_register.plugins())

        if not result_items:
            self.close()
        else:
            self.add_items(result_items)

    def focus_out_event(self, event):
        # 如果当前没有focus的widget就关闭
        widget = QApplication.focusWidget()
        if isinstance(widget, QLineEdit):
            print widget
        if not widget and self.focus_out_close:
            self.close()

    def load_style(self):
        with open('res/theme.css') as f:
            self.setStyleSheet(f.read())

    def show(self):
        self.input_line_edit.setText('')
        super(Quicker, self).show()

    def reload_plugin(self):
        self._plugin_register.reload_plugins()

    def add_items(self, result_items):
        self.result_list_widget.clear()

        for item in result_items:
            self.add_item(item)

        self.update_result_list_height(len(result_items))

    def add_item(self, result_item):
        item = QListWidgetItem()
        item.setSizeHint(QSize(200, self.RESULT_ITEM_HEIGHT))
        self.result_list_widget.addItem(item)
        self.result_list_widget.setItemWidget(item, result_item)


def add_action(menu, name, connect_func, parent, icon=None, shortcut=''):
    if icon:
        action = QAction(QIcon(icon), name, parent)
    else:
        action = QAction(name, parent)
    # todo 设置快捷键不起作用
    action.setShortcut(shortcut)

    action.triggered.connect(connect_func)
    menu.addAction(action)
    return action


def tray_clicked(tray, quicker, reason):
    if reason is tray.Trigger:
        quicker.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    tray = QSystemTrayIcon()
    quicker = Quicker()

    tray.setIcon(QIcon('res/launch.png'))
    menu = QMenu()
    tray.setContextMenu(menu)

    add_action(menu, u'主界面', quicker.show, app, shortcut='Alt+Q')
    add_action(menu, u'重载插件', quicker.reload_plugin, app)
    add_action(menu, u'退出', app.exit, app)

    tray.activated.connect(partial(tray_clicked, tray, quicker))

    tray.show()

    sys.exit(app.exec_())
