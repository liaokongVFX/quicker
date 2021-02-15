# -*- coding: utf-8 -*-
# Time    : 2021/2/15 18:01
# Author  : LiaoKong

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class TranslationWidget(QDialog):
    def __init__(self, src, dst, parent=None):
        super(TranslationWidget, self).__init__(parent)
        self.init_ui(src, dst)

    def init_ui(self, src, dst):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.installEventFilter(self)

        src_label = QLabel(u'<b>原词</b>')
        src_text_edit = QTextEdit()
        src_text_edit.setReadOnly(True)
        src_text_edit.setMaximumHeight(60)
        src_text_edit.setText(src)
        dst_label = QLabel(u'<b>翻译</b>')
        dst_text_edit = QTextEdit()
        dst_text_edit.setReadOnly(True)
        dst_text_edit.setMaximumHeight(100)
        dst_text_edit.setText(dst)

        layout = QVBoxLayout(self)
        layout.addWidget(src_label)
        layout.addWidget(src_text_edit)
        layout.addWidget(dst_label)
        layout.addWidget(dst_text_edit)

    def show_window(self):
        pos = QCursor.pos()
        pos.setY(pos.y() - 50)
        self.move(pos)
        self.show()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.WindowDeactivate:
            self.close()
        return QObject.eventFilter(self, obj, event)  # 交由其他控件处理


if __name__ == '__main__':
    app = QApplication([])
    window = TranslationWidget('aaa','bbbbbb')
    window.show_window()
    app.exec_()

