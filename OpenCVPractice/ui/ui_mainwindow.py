# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QStatusBar,
    QTabWidget, QTextBrowser, QTextEdit, QToolBox,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(981, 600)
        self.actionimport = QAction(MainWindow)
        self.actionimport.setObjectName(u"actionimport")
        icon = QIcon()
        icon.addFile(u"assets/icon/zengjia.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionimport.setIcon(icon)
        self.actionexport = QAction(MainWindow)
        self.actionexport.setObjectName(u"actionexport")
        icon1 = QIcon()
        icon1.addFile(u"assets/icon/jianshao.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionexport.setIcon(icon1)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.menuFrame = QFrame(self.centralwidget)
        self.menuFrame.setObjectName(u"menuFrame")
        self.menuFrame.setFrameShape(QFrame.Box)
        self.menuFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.menuFrame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.introduceBtn = QPushButton(self.menuFrame)
        self.introduceBtn.setObjectName(u"introduceBtn")
        icon2 = QIcon()
        icon2.addFile(u"assets/icon/caidanliebiao.png", QSize(), QIcon.Normal, QIcon.Off)
        self.introduceBtn.setIcon(icon2)

        self.verticalLayout.addWidget(self.introduceBtn)

        self.imgProcessBtn = QPushButton(self.menuFrame)
        self.imgProcessBtn.setObjectName(u"imgProcessBtn")
        icon3 = QIcon()
        icon3.addFile(u"assets/icon/bianji.png", QSize(), QIcon.Normal, QIcon.Off)
        self.imgProcessBtn.setIcon(icon3)

        self.verticalLayout.addWidget(self.imgProcessBtn)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.menuFrame)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setFrameShape(QFrame.Box)
        self.pageIntroduce = QWidget()
        self.pageIntroduce.setObjectName(u"pageIntroduce")
        self.horizontalLayout_3 = QHBoxLayout(self.pageIntroduce)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.introduceTextEdit = QTextEdit(self.pageIntroduce)
        self.introduceTextEdit.setObjectName(u"introduceTextEdit")

        self.horizontalLayout_3.addWidget(self.introduceTextEdit)

        self.stackedWidget.addWidget(self.pageIntroduce)
        self.pageProcess = QWidget()
        self.pageProcess.setObjectName(u"pageProcess")
        self.horizontalLayout_2 = QHBoxLayout(self.pageProcess)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.functionToolBox = QToolBox(self.pageProcess)
        self.functionToolBox.setObjectName(u"functionToolBox")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.functionToolBox.sizePolicy().hasHeightForWidth())
        self.functionToolBox.setSizePolicy(sizePolicy)
        self.functionToolBox.setFrameShape(QFrame.Panel)
        self.imgRepair = QWidget()
        self.imgRepair.setObjectName(u"imgRepair")
        self.imgRepair.setGeometry(QRect(0, 0, 115, 397))
        self.verticalLayout_4 = QVBoxLayout(self.imgRepair)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.pushButton_3 = QPushButton(self.imgRepair)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.verticalLayout_4.addWidget(self.pushButton_3)

        self.pushButton_4 = QPushButton(self.imgRepair)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.verticalLayout_4.addWidget(self.pushButton_4)

        self.functionToolBox.addItem(self.imgRepair, u"\u56fe\u50cf\u4fee\u590d")
        self.imgFilter = QWidget()
        self.imgFilter.setObjectName(u"imgFilter")
        self.verticalLayout_3 = QVBoxLayout(self.imgFilter)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.pushButton_5 = QPushButton(self.imgFilter)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.verticalLayout_3.addWidget(self.pushButton_5)

        self.pushButton_6 = QPushButton(self.imgFilter)
        self.pushButton_6.setObjectName(u"pushButton_6")

        self.verticalLayout_3.addWidget(self.pushButton_6)

        self.functionToolBox.addItem(self.imgFilter, u"\u56fe\u50cf\u8fc7\u6ee4")
        self.imgTransfer = QWidget()
        self.imgTransfer.setObjectName(u"imgTransfer")
        self.imgTransfer.setGeometry(QRect(0, 0, 115, 397))
        self.verticalLayout_7 = QVBoxLayout(self.imgTransfer)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.pushButton_9 = QPushButton(self.imgTransfer)
        self.pushButton_9.setObjectName(u"pushButton_9")

        self.verticalLayout_7.addWidget(self.pushButton_9)

        self.pushButton_14 = QPushButton(self.imgTransfer)
        self.pushButton_14.setObjectName(u"pushButton_14")

        self.verticalLayout_7.addWidget(self.pushButton_14)

        self.functionToolBox.addItem(self.imgTransfer, u"\u56fe\u50cf\u53d8\u6362")

        self.horizontalLayout_2.addWidget(self.functionToolBox)

        self.mainFrame = QFrame(self.pageProcess)
        self.mainFrame.setObjectName(u"mainFrame")
        self.mainFrame.setFrameShape(QFrame.Box)
        self.mainFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.mainFrame)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.imageFrame = QFrame(self.mainFrame)
        self.imageFrame.setObjectName(u"imageFrame")
        self.imageFrame.setFrameShape(QFrame.Box)
        self.imageFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.imageFrame)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label = QLabel(self.imageFrame)
        self.label.setObjectName(u"label")

        self.verticalLayout_8.addWidget(self.label)


        self.verticalLayout_11.addWidget(self.imageFrame)

        self.outputTabWidget = QTabWidget(self.mainFrame)
        self.outputTabWidget.setObjectName(u"outputTabWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.outputTabWidget.sizePolicy().hasHeightForWidth())
        self.outputTabWidget.setSizePolicy(sizePolicy1)
        self.outputTab = QWidget()
        self.outputTab.setObjectName(u"outputTab")
        self.verticalLayout_9 = QVBoxLayout(self.outputTab)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.textBrowser = QTextBrowser(self.outputTab)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout_9.addWidget(self.textBrowser)

        self.outputTabWidget.addTab(self.outputTab, "")
        self.introduceTab = QWidget()
        self.introduceTab.setObjectName(u"introduceTab")
        self.verticalLayout_10 = QVBoxLayout(self.introduceTab)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.textBrowser_2 = QTextBrowser(self.introduceTab)
        self.textBrowser_2.setObjectName(u"textBrowser_2")

        self.verticalLayout_10.addWidget(self.textBrowser_2)

        self.outputTabWidget.addTab(self.introduceTab, "")

        self.verticalLayout_11.addWidget(self.outputTabWidget)


        self.horizontalLayout_2.addWidget(self.mainFrame)

        self.propertiesFrame = QFrame(self.pageProcess)
        self.propertiesFrame.setObjectName(u"propertiesFrame")
        self.propertiesFrame.setFrameShape(QFrame.Box)
        self.propertiesFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.propertiesFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.pushButton_7 = QPushButton(self.propertiesFrame)
        self.pushButton_7.setObjectName(u"pushButton_7")

        self.verticalLayout_2.addWidget(self.pushButton_7)

        self.pushButton_8 = QPushButton(self.propertiesFrame)
        self.pushButton_8.setObjectName(u"pushButton_8")

        self.verticalLayout_2.addWidget(self.pushButton_8)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)


        self.horizontalLayout_2.addWidget(self.propertiesFrame)

        self.stackedWidget.addWidget(self.pageProcess)

        self.horizontalLayout.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 981, 26))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.actionimport)
        self.menu.addAction(self.actionexport)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(1)
        self.functionToolBox.setCurrentIndex(0)
        self.outputTabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionimport.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u5165", None))
        self.actionexport.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fa", None))
        self.introduceBtn.setText(QCoreApplication.translate("MainWindow", u"\u4ecb\u7ecd", None))
        self.imgProcessBtn.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u50cf\u5904\u7406", None))
        self.introduceTextEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Microsoft YaHei UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u5236\u4f5c\u60f3\u6cd5:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u5c1d\u8bd5\u5c06OpenCV\u548cQT\u7ed3\u5408\u8d77\u6765\u5f00\u53d1\u4e00\u4e2a\u53ef\u7528\u7684\u7a0b\u5e8f.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-in"
                        "dent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u8f6f\u4ef6\u4ecb\u7ecd:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u901a\u8fc7opencv\u5bf9\u5bfc\u5165\u7684\u56fe\u7247\u8fdb\u884c\u5904\u7406,\u7136\u540e\u5c06\u7ed3\u679c\u8fdb\u884c\u8f93\u51fa.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u4f7f\u7528\u65b9\u6cd5:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1. \u5bfc\u5165\u56fe\u7247</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block"
                        "-indent:0; text-indent:0px;\">2. \u9009\u62e9\u5408\u9002\u7684\u7b97\u6cd5\u8fdb\u884c\u56fe\u50cf\u5904\u7406</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">3. \u5bfc\u51fa\u56fe\u7247</p></body></html>", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u4fee\u590d1", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"\u4fee\u590d2", None))
        self.functionToolBox.setItemText(self.functionToolBox.indexOf(self.imgRepair), QCoreApplication.translate("MainWindow", u"\u56fe\u50cf\u4fee\u590d", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"\u8fc7\u6ee41", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"\u8fc7\u6ee42", None))
        self.functionToolBox.setItemText(self.functionToolBox.indexOf(self.imgFilter), QCoreApplication.translate("MainWindow", u"\u56fe\u50cf\u8fc7\u6ee4", None))
        self.pushButton_9.setText(QCoreApplication.translate("MainWindow", u"\u53d8\u63621", None))
        self.pushButton_14.setText(QCoreApplication.translate("MainWindow", u"\u53d8\u63622", None))
        self.functionToolBox.setItemText(self.functionToolBox.indexOf(self.imgTransfer), QCoreApplication.translate("MainWindow", u"\u56fe\u50cf\u53d8\u6362", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u653e\u7f6e\u56fe\u7247", None))
        self.textBrowser.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Microsoft YaHei UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u8fd0\u884c\u8f93\u51fa</p></body></html>", None))
        self.outputTabWidget.setTabText(self.outputTabWidget.indexOf(self.outputTab), QCoreApplication.translate("MainWindow", u"\u8fd0\u884c\u8f93\u51fa", None))
        self.textBrowser_2.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Microsoft YaHei UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u7b97\u6cd5\u6587\u5b57\u4ecb\u7ecd</p></body></html>", None))
        self.outputTabWidget.setTabText(self.outputTabWidget.indexOf(self.introduceTab), QCoreApplication.translate("MainWindow", u"\u7b97\u6cd5\u7b80\u4ecb", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"\u7b97\u6cd5\u5c5e\u60271", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"\u7b97\u6cd5\u5c5e\u60271", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u56fe\u7247", None))
    # retranslateUi

