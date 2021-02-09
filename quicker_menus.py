# -*- coding: utf-8 -*-
# Time    : 2021/2/9 20:13
# Author  : LiaoKong

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *


class QuickerMenusWidget(QWidget):
    def __init__(self, title, menus_actions, parent=None):
        super(QuickerMenusWidget, self).__init__(parent)
        self.title = title
        self.menus_action = menus_actions
        self.ACTION_ITEM_HEIGHT = 40

        self.init_ui()

        self.add_items(self.menus_action)

    def init_ui(self):
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(QSize(280, 350))
        self.load_style()

        v_layout = QVBoxLayout(self)
        v_layout.setContentsMargins(0, 0, 0, 0)
        v_layout.setSpacing(0)

        header_widget = QFrame()
        header_widget.setObjectName('header_widget')
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(8, 2, 22, 0)
        icon_label = QLabel()
        icon_label.setFixedSize(32, 32)
        pix_map = QPixmap('res/menus_title.png').scaled(32, 32, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(pix_map)

        self.title_label = QLabel()
        self.title_label.setText(self.title)

        header_layout.addWidget(icon_label)
        header_layout.addItem(QSpacerItem(60, 50, QSizePolicy.Expanding, QSizePolicy.Minimum))
        header_layout.addWidget(self.title_label)

        header_widget.setLayout(header_layout)

        self.action_list_widget = QListWidget()
        self.action_list_widget.setObjectName('action_list_widget')

        v_layout.addWidget(header_widget)
        v_layout.addWidget(self.action_list_widget)
        v_layout.addItem(QSpacerItem(40, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.activateWindow()

    def update_action_list_height(self, action_items_num):
        # list高度需要根据数据个数自动调整
        height = action_items_num * self.ACTION_ITEM_HEIGHT
        if height > 6 * self.ACTION_ITEM_HEIGHT:
            height = 6 * self.ACTION_ITEM_HEIGHT

        self.action_list_widget.setFixedHeight(height)

    def add_items(self, action_items):
        self.action_list_widget.clear()

        for item in action_items:
            self.add_item(item)

        self.update_action_list_height(len(action_items))

    def add_item(self, text):
        item = QListWidgetItem(QIcon('res/launch.png'), text)
        item.setSizeHint(QSize(200, self.ACTION_ITEM_HEIGHT))

        self.action_list_widget.addItem(item)

    def show_window(self):
        pos = QCursor.pos()
        pos.setX(pos.x() - 100)
        pos.setY(pos.y() - 50)
        self.move(pos)
        self.show()

    def load_style(self):
        with open('res/menus_theme.css') as f:
            self.setStyleSheet(f.read())


if __name__ == '__main__':
    app = QApplication([])
    qmw = QuickerMenusWidget(u'已选择1个文件', ['a', 'b', 'c', 'a', ])
    qmw.show_window()
    app.exec_()