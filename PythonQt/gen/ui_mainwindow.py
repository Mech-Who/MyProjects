# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_mainwindow.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QLayout, QLineEdit, QListWidgetItem, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QTabWidget, QToolBox,
    QToolButton, QWidget)

from ModelItem import ModelListWidget
from QtLabelCVWidget import LabelCVWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1077, 600)
        self.actionImport = QAction(MainWindow)
        self.actionImport.setObjectName(u"actionImport")
        icon = QIcon()
        icon.addFile(u"assets/icon/zengjia.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionImport.setIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.modelSelect = QWidget()
        self.modelSelect.setObjectName(u"modelSelect")
        self.gridLayout_4 = QGridLayout(self.modelSelect)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.toolBox = QToolBox(self.modelSelect)
        self.toolBox.setObjectName(u"toolBox")
        self.defaultModel = QWidget()
        self.defaultModel.setObjectName(u"defaultModel")
        self.defaultModel.setGeometry(QRect(0, 0, 686, 437))
        self.gridLayout_6 = QGridLayout(self.defaultModel)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.systemModelListWidget = ModelListWidget(self.defaultModel)
        self.systemModelListWidget.setObjectName(u"systemModelListWidget")

        self.gridLayout_6.addWidget(self.systemModelListWidget, 0, 0, 1, 1)

        self.toolBox.addItem(self.defaultModel, u"\u9ed8\u8ba4\u6a21\u578b")
        self.importModel = QWidget()
        self.importModel.setObjectName(u"importModel")
        self.importModel.setGeometry(QRect(0, 0, 686, 437))
        self.gridLayout_5 = QGridLayout(self.importModel)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.importModelListWidget = ModelListWidget(self.importModel)
        self.importModelListWidget.setObjectName(u"importModelListWidget")

        self.gridLayout_5.addWidget(self.importModelListWidget, 0, 0, 1, 1)

        self.toolBox.addItem(self.importModel, u"\u5bfc\u5165\u6a21\u578b")

        self.gridLayout_4.addWidget(self.toolBox, 0, 0, 1, 1)

        self.modelInfoFrame = QFrame(self.modelSelect)
        self.modelInfoFrame.setObjectName(u"modelInfoFrame")
        self.modelInfoFrame.setFrameShape(QFrame.NoFrame)
        self.modelInfoFrame.setFrameShadow(QFrame.Raised)
        self.gridLayout_8 = QGridLayout(self.modelInfoFrame)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.skeletonBindButton = QPushButton(self.modelInfoFrame)
        self.skeletonBindButton.setObjectName(u"skeletonBindButton")

        self.gridLayout_8.addWidget(self.skeletonBindButton, 9, 1, 1, 2)

        self.horizontalSpacer_4 = QSpacerItem(10, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_4, 9, 6, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_8.addItem(self.verticalSpacer_3, 6, 1, 1, 1)

        self.modelInfoFileLineEdit = QLineEdit(self.modelInfoFrame)
        self.modelInfoFileLineEdit.setObjectName(u"modelInfoFileLineEdit")

        self.gridLayout_8.addWidget(self.modelInfoFileLineEdit, 8, 2, 1, 6)

        self.modelThumbnailLabel = QLabel(self.modelInfoFrame)
        self.modelThumbnailLabel.setObjectName(u"modelThumbnailLabel")

        self.gridLayout_8.addWidget(self.modelThumbnailLabel, 1, 1, 1, 1)

        self.modelInfoNameLabel = QLabel(self.modelInfoFrame)
        self.modelInfoNameLabel.setObjectName(u"modelInfoNameLabel")

        self.gridLayout_8.addWidget(self.modelInfoNameLabel, 7, 1, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(10, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_5, 9, 0, 1, 1)

        self.modelInfoFileLabel = QLabel(self.modelInfoFrame)
        self.modelInfoFileLabel.setObjectName(u"modelInfoFileLabel")

        self.gridLayout_8.addWidget(self.modelInfoFileLabel, 8, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(10, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_3, 9, 3, 1, 1)

        self.modelDefaultButton = QPushButton(self.modelInfoFrame)
        self.modelDefaultButton.setObjectName(u"modelDefaultButton")

        self.gridLayout_8.addWidget(self.modelDefaultButton, 9, 4, 1, 2)

        self.modelDeleteButton = QPushButton(self.modelInfoFrame)
        self.modelDeleteButton.setObjectName(u"modelDeleteButton")

        self.gridLayout_8.addWidget(self.modelDeleteButton, 9, 7, 1, 1)

        self.modelInfoNameLineEdit = QLineEdit(self.modelInfoFrame)
        self.modelInfoNameLineEdit.setObjectName(u"modelInfoNameLineEdit")

        self.gridLayout_8.addWidget(self.modelInfoNameLineEdit, 7, 2, 1, 6)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_8.addItem(self.verticalSpacer_4, 0, 1, 1, 1)

        self.imageLabel = QLabel(self.modelInfoFrame)
        self.imageLabel.setObjectName(u"imageLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageLabel.sizePolicy().hasHeightForWidth())
        self.imageLabel.setSizePolicy(sizePolicy)
        self.imageLabel.setFrameShape(QFrame.NoFrame)
        self.imageLabel.setFrameShadow(QFrame.Plain)

        self.gridLayout_8.addWidget(self.imageLabel, 2, 1, 1, 7)


        self.gridLayout_4.addWidget(self.modelInfoFrame, 0, 1, 1, 1)

        self.gridLayout_4.setColumnStretch(0, 2)
        self.gridLayout_4.setColumnStretch(1, 1)
        self.tabWidget.addTab(self.modelSelect, "")
        self.videoConversion = QWidget()
        self.videoConversion.setObjectName(u"videoConversion")
        self.gridLayout = QGridLayout(self.videoConversion)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout.setHorizontalSpacing(6)
        self.stopVideoRenderButton = QPushButton(self.videoConversion)
        self.stopVideoRenderButton.setObjectName(u"stopVideoRenderButton")

        self.gridLayout.addWidget(self.stopVideoRenderButton, 2, 5, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_6, 2, 0, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_7, 2, 6, 1, 1)

        self.videoFileLabel = QLabel(self.videoConversion)
        self.videoFileLabel.setObjectName(u"videoFileLabel")

        self.gridLayout.addWidget(self.videoFileLabel, 1, 0, 1, 1)

        self.startVideoRenderButton = QPushButton(self.videoConversion)
        self.startVideoRenderButton.setObjectName(u"startVideoRenderButton")

        self.gridLayout.addWidget(self.startVideoRenderButton, 2, 2, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_8, 2, 1, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_9, 2, 7, 1, 1)

        self.fileSelectToolButton = QToolButton(self.videoConversion)
        self.fileSelectToolButton.setObjectName(u"fileSelectToolButton")

        self.gridLayout.addWidget(self.fileSelectToolButton, 1, 7, 1, 1)

        self.videoFileLineEdit = QLineEdit(self.videoConversion)
        self.videoFileLineEdit.setObjectName(u"videoFileLineEdit")

        self.gridLayout.addWidget(self.videoFileLineEdit, 1, 1, 1, 6)

        self.conversionFrame = QFrame(self.videoConversion)
        self.conversionFrame.setObjectName(u"conversionFrame")
        self.conversionFrame.setFrameShape(QFrame.Box)
        self.conversionFrame.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.conversionFrame)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.renderVideoLabel = QLabel(self.conversionFrame)
        self.renderVideoLabel.setObjectName(u"renderVideoLabel")

        self.gridLayout_7.addWidget(self.renderVideoLabel, 0, 3, 1, 1)

        self.videoLabel = QLabel(self.conversionFrame)
        self.videoLabel.setObjectName(u"videoLabel")
        self.videoLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.videoLabel, 0, 0, 1, 1)

        self.renderVideoPandaWidget = QWidget(self.conversionFrame)
        self.renderVideoPandaWidget.setObjectName(u"renderVideoPandaWidget")

        self.gridLayout_7.addWidget(self.renderVideoPandaWidget, 2, 3, 1, 1)

        self.videoWidget = LabelCVWidget(self.conversionFrame)
        self.videoWidget.setObjectName(u"videoWidget")

        self.gridLayout_7.addWidget(self.videoWidget, 2, 0, 1, 2)

        self.gridLayout_7.setRowStretch(2, 1)
        self.gridLayout_7.setColumnStretch(0, 1)
        self.gridLayout_7.setColumnStretch(3, 1)

        self.gridLayout.addWidget(self.conversionFrame, 3, 0, 1, 8)

        self.tabWidget.addTab(self.videoConversion, "")
        self.videoPreView = QWidget()
        self.videoPreView.setObjectName(u"videoPreView")
        self.gridLayout_3 = QGridLayout(self.videoPreView)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.stopPreviewButton = QPushButton(self.videoPreView)
        self.stopPreviewButton.setObjectName(u"stopPreviewButton")

        self.gridLayout_3.addWidget(self.stopPreviewButton, 0, 3, 1, 1)

        self.startPreviewButton = QPushButton(self.videoPreView)
        self.startPreviewButton.setObjectName(u"startPreviewButton")

        self.gridLayout_3.addWidget(self.startPreviewButton, 0, 2, 1, 1)

        self.renderLabel = QLabel(self.videoPreView)
        self.renderLabel.setObjectName(u"renderLabel")

        self.gridLayout_3.addWidget(self.renderLabel, 0, 5, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.cameraLabel = QLabel(self.videoPreView)
        self.cameraLabel.setObjectName(u"cameraLabel")

        self.gridLayout_3.addWidget(self.cameraLabel, 0, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_2, 0, 4, 1, 1)

        self.renderCameraPandaWidget = QWidget(self.videoPreView)
        self.renderCameraPandaWidget.setObjectName(u"renderCameraPandaWidget")

        self.gridLayout_3.addWidget(self.renderCameraPandaWidget, 1, 3, 1, 3)

        self.cameraWidget = LabelCVWidget(self.videoPreView)
        self.cameraWidget.setObjectName(u"cameraWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.cameraWidget.sizePolicy().hasHeightForWidth())
        self.cameraWidget.setSizePolicy(sizePolicy1)

        self.gridLayout_3.addWidget(self.cameraWidget, 1, 0, 1, 3)

        self.tabWidget.addTab(self.videoPreView, "")

        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1077, 21))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.actionImport)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)
        self.toolBox.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionImport.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u5165\u6a21\u578b", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.defaultModel), QCoreApplication.translate("MainWindow", u"\u9ed8\u8ba4\u6a21\u578b", None))
#if QT_CONFIG(tooltip)
        self.toolBox.setItemToolTip(self.toolBox.indexOf(self.defaultModel), QCoreApplication.translate("MainWindow", u"\u7cfb\u7edf\u81ea\u5e26\u7684\u6a21\u578b", None))
#endif // QT_CONFIG(tooltip)
        self.toolBox.setItemText(self.toolBox.indexOf(self.importModel), QCoreApplication.translate("MainWindow", u"\u5bfc\u5165\u6a21\u578b", None))
#if QT_CONFIG(tooltip)
        self.toolBox.setItemToolTip(self.toolBox.indexOf(self.importModel), QCoreApplication.translate("MainWindow", u"\u7528\u6237\u624b\u52a8\u5bfc\u5165\u7684\u6a21\u578b", None))
#endif // QT_CONFIG(tooltip)
        self.skeletonBindButton.setText(QCoreApplication.translate("MainWindow", u"\u9aa8\u9abc\u7ed1\u5b9a", None))
        self.modelThumbnailLabel.setText(QCoreApplication.translate("MainWindow", u"\u6a21\u578b\u7f29\u7565\u56fe\uff1a", None))
        self.modelInfoNameLabel.setText(QCoreApplication.translate("MainWindow", u"\u6a21\u578b\u540d\u79f0\uff1a", None))
        self.modelInfoFileLabel.setText(QCoreApplication.translate("MainWindow", u"\u6a21\u578b\u6587\u4ef6\uff1a", None))
        self.modelDefaultButton.setText(QCoreApplication.translate("MainWindow", u"\u9ed8\u8ba4\u8bbe\u7f6e", None))
        self.modelDeleteButton.setText(QCoreApplication.translate("MainWindow", u"\u5220\u9664\u6a21\u578b", None))
        self.imageLabel.setText(QCoreApplication.translate("MainWindow", u"\u9884\u89c8\u56fe", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.modelSelect), QCoreApplication.translate("MainWindow", u"\u6a21\u578b\u9009\u62e9", None))
        self.stopVideoRenderButton.setText(QCoreApplication.translate("MainWindow", u"\u505c\u6b62\u6e32\u67d3", None))
        self.videoFileLabel.setText(QCoreApplication.translate("MainWindow", u"\u89c6\u9891\u6587\u4ef6\uff1a", None))
        self.startVideoRenderButton.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u6e32\u67d3", None))
        self.fileSelectToolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.renderVideoLabel.setText(QCoreApplication.translate("MainWindow", u"\u6e32\u67d3\u89c6\u9891", None))
        self.videoLabel.setText(QCoreApplication.translate("MainWindow", u"\u539f\u89c6\u9891", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.videoConversion), QCoreApplication.translate("MainWindow", u"\u89c6\u9891\u8f6c\u6362", None))
        self.stopPreviewButton.setText(QCoreApplication.translate("MainWindow", u"\u505c\u6b62\u9884\u89c8", None))
        self.startPreviewButton.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u9884\u89c8", None))
        self.renderLabel.setText(QCoreApplication.translate("MainWindow", u"\u6e32\u67d3\u7ed3\u679c", None))
        self.cameraLabel.setText(QCoreApplication.translate("MainWindow", u"\u6444\u50cf\u5934\u539f\u753b", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.videoPreView), QCoreApplication.translate("MainWindow", u"\u89c6\u9891\u9884\u89c8", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u6a21\u578b", None))
    # retranslateUi

