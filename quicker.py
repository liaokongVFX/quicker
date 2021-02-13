# -*- coding: utf-8 -*-
# Time    : 2021/2/8 20:32
# Author  : LiaoKong
import os
import time

from PySide2.QtWidgets import *
from PySide2.QtCore import *

from notification import NotificationWindow
from core.plugin_register import PluginRegister
from core.action_register import ActionRegister
from timing_tasks_manager import TimingTasksManager
from hotkey import HotkeyThread
from quicker_menus import QuickerMenusWidget
from libs import keyboard
import setting
import utils

log = utils.get_logger(u'Quicker')


class Quicker(QWidget):
    def __init__(self, parent=None):
        super(Quicker, self).__init__(parent)

        self.placeholder = u'请输入关键字'
        self.RESULT_ITEM_HEIGHT = 62
        self.clipboard = QApplication.clipboard()

        pos = QDesktopWidget().availableGeometry().center()
        pos.setX(pos.x() - (self.width() / 2) - 150)
        pos.setY(pos.y() - 350)
        self.move(pos)

        self.init_ui()

        self.plugin_register = PluginRegister(self)
        self.action_register = ActionRegister(self)

        # 定时任务
        self.timing_task_manager = TimingTasksManager()
        self.timing_task_manager.show_msg_sig.connect(self.show_timing_task_msg)

        self.init_hotkey()

        self.update_result_list_height(0)

    @staticmethod
    def show_timing_task_msg(msg):
        NotificationWindow.success(u'提醒', msg)

    def init_hotkey(self):
        global_shortcuts = setting.GLOBAL_HOTKEYS
        plugin_shortcuts = self.plugin_register.get_keyword_by_shortcut()
        if set(global_shortcuts) & set(plugin_shortcuts):
            log.error('There are duplicate shortcuts.')
            log.error(u'global_shortcuts: {}'.format(global_shortcuts))
            log.error(u'plugin_shortcuts: {}'.format(plugin_shortcuts))
            raise ValueError('There are duplicate shortcuts.')
        global_shortcuts.update(self.plugin_register.get_keyword_by_shortcut())

        hotkeys = HotkeyThread(global_shortcuts, self)
        hotkeys.show_main_sign.connect(self.set_visible)
        hotkeys.shortcut_triggered.connect(self.shortcut_triggered)
        hotkeys.start()

    def shortcut_triggered(self, plugin_name):
        if self.plugin_register.get_plugin(plugin_name):
            self.set_show()
            self.input_line_edit.setText(plugin_name + ' ')

        if plugin_name in setting.GLOBAL_HOTKEYS.values():
            getattr(self, plugin_name)()

    def show_menus(self):
        utils.clear_clipboard()
        keyboard.press_and_release('ctrl+c')
        time.sleep(0.25)

        urls = self.clipboard.mimeData().urls()
        urls = [u.toLocalFile() for u in urls if os.path.exists(u.toLocalFile())]
        text = self.clipboard.mimeData().text()

        if not urls and not text:
            data = {
                'type': 'empty'
            }
        elif not urls and text:
            data = {
                'type': 'text',
                'text': text
            }
        else:
            data = {
                'type': 'urls',
                'urls': urls
            }

        log.info(u'已调用quicker menus，{}'.format(data))
        menus_widget = QuickerMenusWidget(data, self)
        menus_widget.show_window()

    def init_ui(self):
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.setFixedSize(QSize(850, 600))

        self.load_style()
        self.installEventFilter(self)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self.input_line_edit = QLineEdit()
        self.input_line_edit.setPlaceholderText(self.placeholder)
        self.input_line_edit.setFocusPolicy(Qt.ClickFocus)
        self.input_line_edit.setMinimumHeight(66)
        self.input_line_edit.returnPressed.connect(self.input_line_edit_return_pressed)
        self.input_line_edit.textChanged.connect(self.input_line_edit_text_changed)

        self.result_list_widget = QListWidget()
        self.result_list_widget.setObjectName('result_list_widget')
        self.result_list_widget.setFocusPolicy(Qt.ClickFocus)
        self.result_list_widget.keyPressEvent = self.result_list_key_press_event
        self.result_list_widget.itemClicked.connect(self.execute_result_item)

        layout.addWidget(self.input_line_edit)
        layout.addWidget(self.result_list_widget)
        layout.addItem(QSpacerItem(40, 100, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.input_line_edit.setFocus(Qt.MouseFocusReason)

        self.set_visible()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.WindowDeactivate:
            self.set_visible()
        return QObject.eventFilter(self, obj, event)  # 交由其他控件处理

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
            result_items = self.plugin_register.search_plugin(plugin_keyword)
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
        if event.key() == Qt.Key_Escape:
            self.set_visible()

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
                return

        return super(Quicker, self).keyPressEvent(event)

    def result_list_key_press_event(self, event):
        if event.key() == Qt.Key_Return:
            return self.execute_result_item(self.result_list_widget.currentItem())

        super(QListWidget, self.result_list_widget).keyPressEvent(event)

    def execute_result_item(self, item):
        result_item = self.result_list_widget.itemWidget(item)
        if not result_item:
            return

        input_text = self.input_line_edit.text().strip()
        if result_item.keyword and (
                input_text == result_item.keyword or not input_text.startswith(result_item.keyword)):
            self.input_line_edit.setText(result_item.keyword + ' ')
            self.input_line_edit.setFocus(Qt.MouseFocusReason)
            self.result_list_widget.setCurrentRow(-1)
        else:
            self.input_line_edit_return_pressed()

    def input_line_edit_return_pressed(self):
        if self.result_list_widget.count() < 1:
            return

        text = self.input_line_edit.text().strip()
        if len(text.split(' ', 1)) == 2:
            plugin_keyword, execute_str = text.strip().split(' ', 1)
        else:
            plugin_keyword = next(iter(
                self.result_list_widget.itemWidget(self.result_list_widget.item(i)).keyword
                for i in range(self.result_list_widget.count()) if
                self.result_list_widget.itemWidget(self.result_list_widget.item(i)).keyword == text
            ), '')
            execute_str = ''

        if not plugin_keyword:
            return

        result_items = self.plugin_register.execute(plugin_keyword, execute_str, self.plugin_register.plugins())

        if not result_items:
            self.close()
        else:
            self.add_items(result_items)

    def load_style(self):
        with open('res/theme.css') as f:
            self.setStyleSheet(f.read())

    def show(self):
        self.input_line_edit.setText('')
        super(Quicker, self).show()

    def reload_plugin(self):
        self.plugin_register.reload_plugins()

    def reload_actions(self):
        self.action_register.reload_actions()

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

    def set_visible(self):
        if self.isVisible():
            self.input_line_edit.setText('')
            self.setVisible(False)
        else:
            self.set_show()

    def set_show(self):
        self.setVisible(True)
        self.activateWindow()
        self.input_line_edit.setFocus(Qt.MouseFocusReason)
