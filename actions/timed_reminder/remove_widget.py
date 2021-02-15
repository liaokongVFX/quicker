# -*- coding: utf-8 -*-
# Time    : 2021/2/15 16:19
# Author  : LiaoKong

from PySide2.QtWidgets import *

from libs import qflat


class RemoveTimedReminderWidget(QDialog):
    def __init__(self, remind_by_id, parent=None):
        super(RemoveTimedReminderWidget, self).__init__(parent)

        self.remind_by_id = remind_by_id
        self.remove_ids = []
        self._remove_ids = []

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.remind_list_widget = QListWidget()
        for remind_id, remind in self.remind_by_id.items():
            item = QListWidgetItem(remind)
            item.remind_id = remind_id
            self.remind_list_widget.addItem(item)

        del_layout = QHBoxLayout()
        self.remove_btn = QPushButton(u'删除')
        self.remove_btn.clicked.connect(self.remove_btn_clicked)
        self.save_btn = QPushButton(u'保存')
        self.save_btn.clicked.connect(self.save_btn_clicked)
        del_layout.addWidget(self.remove_btn)
        del_layout.addWidget(self.save_btn)
        layout.addWidget(self.remind_list_widget)
        layout.addLayout(del_layout)

    def remove_btn_clicked(self):
        if not self.remind_list_widget.selectedItems():
            return qflat.error(u'请先选择要删除的项')
        self._remove_ids.append(self.remind_list_widget.currentItem().remind_id)
        self.remind_list_widget.takeItem(self.remind_list_widget.currentRow())

    def save_btn_clicked(self):
        self.remove_ids = self._remove_ids
        self.close()


if __name__ == '__main__':
    app = QApplication([])
    window = RemoveTimedReminderWidget({u'删除': 1})
    window.show()
    app.exec_()
