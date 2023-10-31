# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_importmodel.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QGridLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QToolButton, QWidget)

class Ui_ImportModel(object):
    def setupUi(self, ImportModel):
        if not ImportModel.objectName():
            ImportModel.setObjectName(u"ImportModel")
        ImportModel.resize(270, 320)
        self.gridLayout = QGridLayout(ImportModel)
        self.gridLayout.setObjectName(u"gridLayout")
        self.fileFormatLabel = QLabel(ImportModel)
        self.fileFormatLabel.setObjectName(u"fileFormatLabel")

        self.gridLayout.addWidget(self.fileFormatLabel, 1, 0, 1, 1)

        self.fileSelectToolButton = QToolButton(ImportModel)
        self.fileSelectToolButton.setObjectName(u"fileSelectToolButton")

        self.gridLayout.addWidget(self.fileSelectToolButton, 2, 3, 1, 1)

        self.imageFrame = QFrame(ImportModel)
        self.imageFrame.setObjectName(u"imageFrame")
        self.imageFrame.setFrameShape(QFrame.Box)
        self.imageFrame.setFrameShadow(QFrame.Raised)
        self.imageLabel = QLabel(self.imageFrame)
        self.imageLabel.setObjectName(u"imageLabel")
        self.imageLabel.setGeometry(QRect(0, 0, 251, 161))
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageLabel.sizePolicy().hasHeightForWidth())
        self.imageLabel.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.imageFrame, 4, 0, 1, 4)

        self.modelNameLineEdit = QLineEdit(ImportModel)
        self.modelNameLineEdit.setObjectName(u"modelNameLineEdit")

        self.gridLayout.addWidget(self.modelNameLineEdit, 0, 1, 1, 3)

        self.importButton = QPushButton(ImportModel)
        self.importButton.setObjectName(u"importButton")

        self.gridLayout.addWidget(self.importButton, 6, 1, 1, 1)

        self.modelFileLineEdit = QLineEdit(ImportModel)
        self.modelFileLineEdit.setObjectName(u"modelFileLineEdit")

        self.gridLayout.addWidget(self.modelFileLineEdit, 2, 1, 1, 2)

        self.modelNameLabel = QLabel(ImportModel)
        self.modelNameLabel.setObjectName(u"modelNameLabel")

        self.gridLayout.addWidget(self.modelNameLabel, 0, 0, 1, 1)

        self.fileFormatComboBox = QComboBox(ImportModel)
        self.fileFormatComboBox.setObjectName(u"fileFormatComboBox")

        self.gridLayout.addWidget(self.fileFormatComboBox, 1, 1, 1, 3)

        self.cancelButton = QPushButton(ImportModel)
        self.cancelButton.setObjectName(u"cancelButton")

        self.gridLayout.addWidget(self.cancelButton, 6, 2, 1, 1)

        self.modelFileLabel = QLabel(ImportModel)
        self.modelFileLabel.setObjectName(u"modelFileLabel")

        self.gridLayout.addWidget(self.modelFileLabel, 2, 0, 1, 1)

        self.imageFilelabel = QLabel(ImportModel)
        self.imageFilelabel.setObjectName(u"imageFilelabel")

        self.gridLayout.addWidget(self.imageFilelabel, 3, 0, 1, 1)

        self.imageFileLineEdit = QLineEdit(ImportModel)
        self.imageFileLineEdit.setObjectName(u"imageFileLineEdit")

        self.gridLayout.addWidget(self.imageFileLineEdit, 3, 1, 1, 2)

        self.imageFileToolButton = QToolButton(ImportModel)
        self.imageFileToolButton.setObjectName(u"imageFileToolButton")

        self.gridLayout.addWidget(self.imageFileToolButton, 3, 3, 1, 1)


        self.retranslateUi(ImportModel)

        QMetaObject.connectSlotsByName(ImportModel)
    # setupUi

    def retranslateUi(self, ImportModel):
        ImportModel.setWindowTitle(QCoreApplication.translate("ImportModel", u"Dialog", None))
        self.fileFormatLabel.setText(QCoreApplication.translate("ImportModel", u"\u6587\u4ef6\u683c\u5f0f\uff1a", None))
        self.fileSelectToolButton.setText(QCoreApplication.translate("ImportModel", u"...", None))
        self.imageLabel.setText("")
        self.importButton.setText(QCoreApplication.translate("ImportModel", u"\u5bfc\u5165", None))
        self.modelNameLabel.setText(QCoreApplication.translate("ImportModel", u"\u6a21\u578b\u540d\u79f0\uff1a", None))
        self.cancelButton.setText(QCoreApplication.translate("ImportModel", u"\u53d6\u6d88", None))
        self.modelFileLabel.setText(QCoreApplication.translate("ImportModel", u"\u6a21\u578b\u6587\u4ef6\uff1a", None))
        self.imageFilelabel.setText(QCoreApplication.translate("ImportModel", u"\u56fe\u7247\u6587\u4ef6\uff1a", None))
        self.imageFileToolButton.setText(QCoreApplication.translate("ImportModel", u"...", None))
    # retranslateUi

