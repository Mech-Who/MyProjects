# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_modeldefault.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QHeaderView,
    QLabel, QSizePolicy, QSpacerItem, QTreeWidgetItem,
    QWidget)

from QtJsonTreeWidget import JsonTreeWidget
from QtPandaWidget import QtPandaWidget

class Ui_ModelDefault(object):
    def setupUi(self, ModelDefault):
        if not ModelDefault.objectName():
            ModelDefault.setObjectName(u"ModelDefault")
        ModelDefault.resize(1041, 608)
        self.gridLayout = QGridLayout(ModelDefault)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 1, 1, 1)

        self.middleSkeletonLabel = QLabel(ModelDefault)
        self.middleSkeletonLabel.setObjectName(u"middleSkeletonLabel")

        self.gridLayout.addWidget(self.middleSkeletonLabel, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 4, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 1, 5, 1, 1)

        self.defaultPandaWidget = QtPandaWidget(ModelDefault)
        self.defaultPandaWidget.setObjectName(u"defaultPandaWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.defaultPandaWidget.sizePolicy().hasHeightForWidth())
        self.defaultPandaWidget.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.defaultPandaWidget, 3, 4, 1, 2)

        self.horizontalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 1, 2, 1, 1)

        self.jsonTreeWidget = JsonTreeWidget(ModelDefault)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"Key");
        self.jsonTreeWidget.setHeaderItem(__qtreewidgetitem)
        self.jsonTreeWidget.setObjectName(u"jsonTreeWidget")

        self.gridLayout.addWidget(self.jsonTreeWidget, 3, 0, 1, 3)


        self.retranslateUi(ModelDefault)

        QMetaObject.connectSlotsByName(ModelDefault)
    # setupUi

    def retranslateUi(self, ModelDefault):
        ModelDefault.setWindowTitle(QCoreApplication.translate("ModelDefault", u"Dialog", None))
        self.middleSkeletonLabel.setText(QCoreApplication.translate("ModelDefault", u"\u5f53\u524d\u6a21\u578b\u9ed8\u8ba4\u503c", None))
        ___qtreewidgetitem = self.jsonTreeWidget.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("ModelDefault", u"Type", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("ModelDefault", u"Value", None));
    # retranslateUi

