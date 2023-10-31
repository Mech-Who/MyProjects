# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_modelitem.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QMainWindow, QSizePolicy,
    QWidget)

class Ui_WidgetItem(object):
    def setupUi(self, WidgetItem):
        if not WidgetItem.objectName():
            WidgetItem.setObjectName(u"WidgetItem")
        WidgetItem.resize(210, 210)
        self.actionimport = QAction(WidgetItem)
        self.actionimport.setObjectName(u"actionimport")
        icon = QIcon()
        icon.addFile(u"assets/icon/zengjia.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionimport.setIcon(icon)
        self.centralwidget = QWidget(WidgetItem)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        WidgetItem.setCentralWidget(self.centralwidget)

        self.retranslateUi(WidgetItem)

        QMetaObject.connectSlotsByName(WidgetItem)
    # setupUi

    def retranslateUi(self, WidgetItem):
        WidgetItem.setWindowTitle(QCoreApplication.translate("WidgetItem", u"MainWindow", None))
        self.actionimport.setText(QCoreApplication.translate("WidgetItem", u"\u5bfc\u5165\u6a21\u578b", None))
    # retranslateUi

