# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(442, 167)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.date_radio = QRadioButton(Dialog)
        self.date_radio.setObjectName(u"date_radio")

        self.horizontalLayout.addWidget(self.date_radio)

        self.date_time_edit = QDateTimeEdit(Dialog)
        self.date_time_edit.setObjectName(u"date_time_edit")

        self.horizontalLayout.addWidget(self.date_time_edit)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.interval_radio = QRadioButton(Dialog)
        self.interval_radio.setObjectName(u"interval_radio")

        self.horizontalLayout_2.addWidget(self.interval_radio)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.interval_spin = QSpinBox(Dialog)
        self.interval_spin.setObjectName(u"interval_spin")

        self.horizontalLayout_2.addWidget(self.interval_spin)

        self.interval_combo = QComboBox(Dialog)
        self.interval_combo.addItem("")
        self.interval_combo.addItem("")
        self.interval_combo.addItem("")
        self.interval_combo.setObjectName(u"interval_combo")

        self.horizontalLayout_2.addWidget(self.interval_combo)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.cron_radio = QRadioButton(Dialog)
        self.cron_radio.setObjectName(u"cron_radio")

        self.horizontalLayout_3.addWidget(self.cron_radio)

        self.cron_line_edit = QLineEdit(Dialog)
        self.cron_line_edit.setObjectName(u"cron_line_edit")

        self.horizontalLayout_3.addWidget(self.cron_line_edit)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.remind_line_edit = QLineEdit(Dialog)
        self.remind_line_edit.setObjectName(u"remind_line_edit")

        self.horizontalLayout_4.addWidget(self.remind_line_edit)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, -1, 16, -1)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.add_btn = QPushButton(Dialog)
        self.add_btn.setObjectName(u"add_btn")
        self.add_btn.setMinimumSize(QSize(150, 35))

        self.horizontalLayout_5.addWidget(self.add_btn)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", "添加定时提醒", None))
        self.date_radio.setText(QCoreApplication.translate("Dialog", "提醒一次", None))
        self.interval_radio.setText(QCoreApplication.translate("Dialog", "间隔提醒", None))
        self.label.setText(QCoreApplication.translate("Dialog", "每隔", None))
        self.interval_combo.setItemText(0, QCoreApplication.translate("Dialog", "分钟", None))
        self.interval_combo.setItemText(1, QCoreApplication.translate("Dialog", "小时", None))
        self.interval_combo.setItemText(2, QCoreApplication.translate("Dialog", "天", None))

        self.label_2.setText(QCoreApplication.translate("Dialog", "提醒一次", None))
        self.cron_radio.setText(QCoreApplication.translate("Dialog", "周期提醒", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", "提醒内容:", None))
        self.add_btn.setText(QCoreApplication.translate("Dialog", "添加", None))
    # retranslateUi

