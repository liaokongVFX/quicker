# -*- coding: utf-8 -*-
# Time    : 2021/1/27 20:40
# Author  : LiaoKong
import sys

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *


class ResultItem(QWidget):
    def __init__(self, title, description, keyword='', icon='', date_time='', checkbox=None, parent=None):
        super(ResultItem, self).__init__(parent)

        self.title = title
        self.description = description
        self.keyword = keyword
        self.icon = icon
        self.date_time = date_time  # int list,eg:[2021, 1, 21, 15, 21, 11]
        self.checkbox = checkbox

        self.init_ui()

    def init_ui(self):
        self.setObjectName('result_item')
        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, 5, 5, 5)
        self.main_layout.setSpacing(12)

        self.img_label = QLabel()
        self.img_label.setObjectName('img_label')
        self.img_label.setFixedSize(60, 60)
        if self.icon:
            pix_map = QPixmap(self.icon).scaled(50, 50, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            self.img_label.setPixmap(pix_map)
        else:
            self.img_label.setText(self.keyword)

        self.body_layout = QVBoxLayout()
        self.body_layout.setSpacing(0)

        self.title_layout = QHBoxLayout()
        self.title_label = QLabel()
        self.title_label.setObjectName('title_label')
        if self.keyword:
            self.title_label.setText(u'{} ({})'.format(self.title, self.keyword))
        else:
            self.title_label.setText(self.title)
        self.title_layout.addWidget(self.title_label)
        if self.date_time:
            self.date_time_edit = QDateTimeEdit()
            self.date_time_edit.setDateTime(QDateTime(*self.date_time))
            self.title_layout.addWidget(self.date_time_edit)
        self.title_layout.addItem(QSpacerItem(120, 30, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.description_label = QLabel()
        self.description_label.setObjectName('description_label')
        self.description_label.setText(self.description)

        self.body_layout.addLayout(self.title_layout)
        self.body_layout.addWidget(self.description_label)

        self.main_layout.addWidget(self.img_label)
        self.main_layout.addLayout(self.body_layout)
        if self.checkbox is not None:
            self.todo_checkbox = QCheckBox()
            self.todo_checkbox.setChecked(self.checkbox)
            self.main_layout.addWidget(self.todo_checkbox)

        self.load_style()

    def load_style(self):
        with open('res/result_item.css') as f:
            self.setStyleSheet(f.read())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ri = ResultItem(u'百度搜索', u'快速进行百度搜索', 'plugins/a.jpg')
    ri.show()

    sys.exit(app.exec_())
