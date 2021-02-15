# -*- coding: utf-8 -*-
# Time    : 2021/2/15 20:49
# Author  : LiaoKong
from functools import partial

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from libs import keyboard

shortcut = 'p'


class PickColorWidget(QDialog):
    def __init__(self, parent=None):
        super(PickColorWidget, self).__init__(parent)
        self.init_ui()

        keyboard.add_hotkey(shortcut, self.pick_color)

    def pick_color(self):
        pos = QCursor().pos()
        x, y = pos.x(), pos.y()
        pixmap = QApplication.primaryScreen().grabWindow(
            QApplication.desktop().winId(), x, y, 1, 1
        )
        img = pixmap.toImage()
        color = QColor(img.pixel(0, 0))
        r, g, b = color.red(), color.green(), color.blue()
        rgb = '{:^3d},{:^3d},{:^3d}'.format(r, g, b)

        hexs = list(map(lambda x: str(hex(x).replace('0x', '').upper()), [r, g, b]))
        css = '#{:0>2s}{:0>2s}{:0>2s}'.format(*hexs)

        self.label.setStyleSheet('background-color: {}'.format(css))

        self.rgb_btn.setText(u'点击复制 ({})'.format(rgb))
        self.rgb_btn.color = rgb
        self.css_btn.setText(u'点击复制 {}'.format(css))
        self.css_btn.color = css

        self.update()

    def init_ui(self):
        self.setWindowTitle(u'按P键拾取鼠标所在位置颜色')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.resize(QSize(300, 100))
        self.setFocusPolicy(Qt.ClickFocus)

        layout = QHBoxLayout(self)
        layout.setSpacing(2)

        self.label = QLabel()
        self.label.setAutoFillBackground(True)

        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(3)
        self.rgb_btn = QPushButton()
        self.rgb_btn.setMinimumHeight(35)
        self.rgb_btn.clicked.connect(partial(self.copy_btn_clicked, self.rgb_btn))
        self.css_btn = QPushButton()
        self.css_btn.setMinimumHeight(35)
        self.css_btn.clicked.connect(partial(self.copy_btn_clicked, self.css_btn))
        btn_layout.addWidget(self.rgb_btn)
        btn_layout.addWidget(self.css_btn)

        layout.addWidget(self.label)
        layout.addLayout(btn_layout)

    def copy_btn_clicked(self, btn):
        QApplication.clipboard().setText(btn.color)
        keyboard.remove_hotkey(self.pick_color)
        self.close()


if __name__ == '__main__':
    app = QApplication([])
    window = PickColorWidget()
    window.show()
    app.exec_()
