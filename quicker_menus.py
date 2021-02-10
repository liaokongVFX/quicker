# -*- coding: utf-8 -*-
# Time    : 2021/2/9 20:13
# Author  : LiaoKong
import os

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from core import action_base


class QuickerMenusWidget(QWidget):
    def __init__(self, raw_data, parent=None):
        super(QuickerMenusWidget, self).__init__(parent)
        self.raw_data = raw_data
        self.title = u'没有选中文件或文字'
        self.action_type = action_base.EMPTY
        self.data = ''
        self.ACTION_ITEM_HEIGHT = 40

        self.init_data()
        self.init_ui()
        self.init_list_widget()

    def init_list_widget(self):
        items = self.parent().action_register.get_actions(self.action_type)
        if self.action_type == action_base.FILE:
            items = [i for i in items if not i.exts or self.raw_data['urls'][0].lower().endswith(tuple(i.exts))]

        self.add_items(items)

    def init_data(self):
        if self.raw_data['type'] == 'text':
            self.title = u'已选中{}个字'.format(len(self.raw_data['text']))
            self.action_type = action_base.TEXT
            self.data = self.raw_data['text']
        elif self.raw_data['type'] == 'urls':
            urls_num = len(self.raw_data['urls'])
            self.data = self.raw_data['urls']
            if urls_num == 1:
                file_name = os.path.basename(self.raw_data['urls'][0])
                if os.path.isfile(self.raw_data['urls'][0]):
                    file_name = file_name.rsplit('.', 1)[0]
                self.title = u'已选中 {}'.format(file_name)
                self.action_type = action_base.FILE
            else:
                self.title = u'已选中{}个文件'.format(urls_num)
                self.action_type = action_base.MULT_FILES

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
        header_layout.setContentsMargins(8, 2, 12, 0)
        icon_label = QLabel()
        icon_label.setFixedSize(32, 32)
        pix_map = QPixmap('res/menus_title.png').scaled(32, 32, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(pix_map)

        self.title_label = QLabel()
        self.title_label.setText(self.title)
        self.title_label.setToolTip('\n'.join(self.data) if isinstance(self.data, list) else self.data)

        header_layout.addWidget(icon_label)
        header_layout.addItem(QSpacerItem(60, 50, QSizePolicy.Expanding, QSizePolicy.Minimum))
        header_layout.addWidget(self.title_label)

        header_widget.setLayout(header_layout)

        self.action_list_widget = QListWidget()
        self.action_list_widget.setObjectName('action_list_widget')
        self.action_list_widget.itemClicked.connect(self.action_list_widget_item_clicked)

        v_layout.addWidget(header_widget)
        v_layout.addWidget(self.action_list_widget)
        v_layout.addItem(QSpacerItem(40, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.activateWindow()
        self.update_action_list_height(0)

    def action_list_widget_item_clicked(self, item):
        self.close()
        item.action_obj.run(self.data)

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

    def add_item(self, action_obj):
        item = QListWidgetItem(QIcon(action_obj.icon_path), action_obj.title)
        item.setSizeHint(QSize(200, self.ACTION_ITEM_HEIGHT))
        item.setToolTip(action_obj.description)
        item.action_obj = action_obj

        self.action_list_widget.addItem(item)

    def show_window(self):
        pos = QCursor.pos()
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
