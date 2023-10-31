# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_testpanda3d.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QSizePolicy,
    QWidget)

class Ui_PandaWidget(object):
    def setupUi(self, PandaWidget):
        if not PandaWidget.objectName():
            PandaWidget.setObjectName(u"PandaWidget")
        PandaWidget.resize(544, 313)
        self.gridLayout = QGridLayout(PandaWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pandaFrame = QFrame(PandaWidget)
        self.pandaFrame.setObjectName(u"pandaFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pandaFrame.sizePolicy().hasHeightForWidth())
        self.pandaFrame.setSizePolicy(sizePolicy)
        self.pandaFrame.setFrameShape(QFrame.Box)
        self.pandaFrame.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.pandaFrame, 0, 0, 1, 2)


        self.retranslateUi(PandaWidget)

        QMetaObject.connectSlotsByName(PandaWidget)
    # setupUi

    def retranslateUi(self, PandaWidget):
        PandaWidget.setWindowTitle(QCoreApplication.translate("PandaWidget", u"Dialog", None))
    # retranslateUi

