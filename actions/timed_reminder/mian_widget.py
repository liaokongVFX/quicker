# -*- coding: utf-8 -*-
# Time    : 2021/2/14 16:42
# Author  : LiaoKong
from datetime import datetime

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from libs import qflat

from ui.ui import Ui_Dialog


class TimedReminderWidget(QDialog, Ui_Dialog):
    def __init__(self, remind_default='', parent=None):
        super(TimedReminderWidget, self).__init__(parent)
        self.data = {}
        self.setupUi(self)
        self.date_time_edit.setDateTime(datetime.now())
        self.remind_line_edit.setText(remind_default)
        self.cron_line_edit.setPlaceholderText(u'请用键=值,键=值的规则来设置')

        self.add_btn.clicked.connect(self.add_btn_clicked)

    def add_btn_clicked(self):
        remind_text = self.remind_line_edit.text().strip()
        if not remind_text:
            return qflat.error(u'请设置提醒内容')

        if self.date_radio.isChecked():
            self.data = {
                'trigger': 'date',
                'run_date': self.date_time_edit.dateTime().toPython()
            }
        elif self.interval_radio.isChecked():
            en_by_ch = {
                u'天': 'days',
                u'小时': 'hours',
                u'分钟': 'minutes'
            }
            interval_text = self.interval_combo.currentText()
            interval_time = self.interval_spin.text().strip()
            if not interval_time:
                return qflat.error(u'请设置间隔时间')
            self.data = {
                'trigger': 'interval',
                en_by_ch.get(interval_text): int(interval_time)
            }
        elif self.cron_radio.isChecked():
            cron_text = self.cron_line_edit.text().strip()
            try:
                self.data = eval('dict({})'.format(cron_text))
                self.data.update({'trigger': 'cron'})
            except:
                return qflat.error(u'周期提醒格式不对（键=值,键=值）')
        else:
            return qflat.error(u'请先选择要设置提醒的类型')

        self.data.update({'msg': remind_text})
        self.close()


if __name__ == '__main__':
    app = QApplication([])
    window = TimedReminderWidget()
    window.show()
    app.exec_()
