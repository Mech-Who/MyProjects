# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_skeletonmap.ui'
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
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QTreeWidget, QTreeWidgetItem,
    QWidget)

class Ui_SkeletonMapping(object):
    def setupUi(self, SkeletonMapping):
        if not SkeletonMapping.objectName():
            SkeletonMapping.setObjectName(u"SkeletonMapping")
        SkeletonMapping.resize(983, 468)
        self.gridLayout = QGridLayout(SkeletonMapping)
        self.gridLayout.setObjectName(u"gridLayout")
        self.middleSkeletonLabel = QLabel(SkeletonMapping)
        self.middleSkeletonLabel.setObjectName(u"middleSkeletonLabel")

        self.gridLayout.addWidget(self.middleSkeletonLabel, 0, 0, 1, 1)

        self.bindButton = QPushButton(SkeletonMapping)
        self.bindButton.setObjectName(u"bindButton")

        self.gridLayout.addWidget(self.bindButton, 0, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.middleSkeletonTableWidget = QTableWidget(SkeletonMapping)
        if (self.middleSkeletonTableWidget.columnCount() < 4):
            self.middleSkeletonTableWidget.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.middleSkeletonTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.middleSkeletonTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.middleSkeletonTableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.middleSkeletonTableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        if (self.middleSkeletonTableWidget.rowCount() < 16):
            self.middleSkeletonTableWidget.setRowCount(16)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.middleSkeletonTableWidget.setVerticalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.middleSkeletonTableWidget.setVerticalHeaderItem(1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.middleSkeletonTableWidget.setVerticalHeaderItem(2, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.middleSkeletonTableWidget.setVerticalHeaderItem(3, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.middleSkeletonTableWidget.setVerticalHeaderItem(4, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.middleSkeletonTableWidget.setVerticalHeaderItem(5, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.middleSkeletonTableWidget.setVerticalHeaderItem(6, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.middleSkeletonTableWidget.setVerticalHeaderItem(7, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.middleSkeletonTableWidget.setVerticalHeaderItem(8, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.middleSkeletonTableWidget.setVerticalHeaderItem(9, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.middleSkeletonTableWidget.setVerticalHeaderItem(10, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.middleSkeletonTableWidget.setVerticalHeaderItem(11, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.middleSkeletonTableWidget.setVerticalHeaderItem(12, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.middleSkeletonTableWidget.setVerticalHeaderItem(13, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.middleSkeletonTableWidget.setVerticalHeaderItem(14, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.middleSkeletonTableWidget.setVerticalHeaderItem(15, __qtablewidgetitem19)
        self.middleSkeletonTableWidget.setObjectName(u"middleSkeletonTableWidget")

        self.gridLayout.addWidget(self.middleSkeletonTableWidget, 1, 0, 1, 4)

        self.modelSkeletonLabel = QLabel(SkeletonMapping)
        self.modelSkeletonLabel.setObjectName(u"modelSkeletonLabel")

        self.gridLayout.addWidget(self.modelSkeletonLabel, 0, 4, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 5, 1, 1)

        self.modelSkeletonTreeWidget = QTreeWidget(SkeletonMapping)
        self.modelSkeletonTreeWidget.setObjectName(u"modelSkeletonTreeWidget")

        self.gridLayout.addWidget(self.modelSkeletonTreeWidget, 1, 4, 1, 2)


        self.retranslateUi(SkeletonMapping)

        QMetaObject.connectSlotsByName(SkeletonMapping)
    # setupUi

    def retranslateUi(self, SkeletonMapping):
        SkeletonMapping.setWindowTitle(QCoreApplication.translate("SkeletonMapping", u"Dialog", None))
        self.middleSkeletonLabel.setText(QCoreApplication.translate("SkeletonMapping", u"\u4e2d\u95f4\u9aa8\u9abc", None))
        self.bindButton.setText(QCoreApplication.translate("SkeletonMapping", u"\u7ed1\u5b9a", None))
        ___qtablewidgetitem = self.middleSkeletonTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("SkeletonMapping", u"\u6a21\u578b\u7ed1\u5b9a\u9aa8\u9abc", None));
        ___qtablewidgetitem1 = self.middleSkeletonTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("SkeletonMapping", u"fx", None));
        ___qtablewidgetitem2 = self.middleSkeletonTableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("SkeletonMapping", u"fy", None));
        ___qtablewidgetitem3 = self.middleSkeletonTableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("SkeletonMapping", u"fz", None));
        ___qtablewidgetitem4 = self.middleSkeletonTableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("SkeletonMapping", u"Neck", None));
        ___qtablewidgetitem5 = self.middleSkeletonTableWidget.verticalHeaderItem(1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("SkeletonMapping", u"Chest", None));
        ___qtablewidgetitem6 = self.middleSkeletonTableWidget.verticalHeaderItem(2)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("SkeletonMapping", u"Spine", None));
        ___qtablewidgetitem7 = self.middleSkeletonTableWidget.verticalHeaderItem(3)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("SkeletonMapping", u"Hips", None));
        ___qtablewidgetitem8 = self.middleSkeletonTableWidget.verticalHeaderItem(4)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("SkeletonMapping", u"LeftUpperLeg", None));
        ___qtablewidgetitem9 = self.middleSkeletonTableWidget.verticalHeaderItem(5)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("SkeletonMapping", u"LeftLowerLeg", None));
        ___qtablewidgetitem10 = self.middleSkeletonTableWidget.verticalHeaderItem(6)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("SkeletonMapping", u"RightUpperLeg", None));
        ___qtablewidgetitem11 = self.middleSkeletonTableWidget.verticalHeaderItem(7)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("SkeletonMapping", u"RightLowerLeg", None));
        ___qtablewidgetitem12 = self.middleSkeletonTableWidget.verticalHeaderItem(8)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("SkeletonMapping", u"LeftFoot", None));
        ___qtablewidgetitem13 = self.middleSkeletonTableWidget.verticalHeaderItem(9)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("SkeletonMapping", u"RightFoot", None));
        ___qtablewidgetitem14 = self.middleSkeletonTableWidget.verticalHeaderItem(10)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("SkeletonMapping", u"LeftUpperArm", None));
        ___qtablewidgetitem15 = self.middleSkeletonTableWidget.verticalHeaderItem(11)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("SkeletonMapping", u"LeftLowerArm", None));
        ___qtablewidgetitem16 = self.middleSkeletonTableWidget.verticalHeaderItem(12)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("SkeletonMapping", u"RightUpperArm", None));
        ___qtablewidgetitem17 = self.middleSkeletonTableWidget.verticalHeaderItem(13)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("SkeletonMapping", u"RightLowerArm", None));
        ___qtablewidgetitem18 = self.middleSkeletonTableWidget.verticalHeaderItem(14)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("SkeletonMapping", u"LeftHand", None));
        ___qtablewidgetitem19 = self.middleSkeletonTableWidget.verticalHeaderItem(15)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("SkeletonMapping", u"RightHand", None));
        self.modelSkeletonLabel.setText(QCoreApplication.translate("SkeletonMapping", u"\u6a21\u578b\u9aa8\u9abc", None))
        ___qtreewidgetitem = self.modelSkeletonTreeWidget.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("SkeletonMapping", u"\u6a21\u578b\u9aa8\u9abc", None));
    # retranslateUi

