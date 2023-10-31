# This Python file uses the following encoding: utf-8

import json
import pprint

import utils
from QtPandaWidget import PandaHandler, QtPandaWidget
from QtJsonTreeWidget import JsonTreeWidget, JsonTreeWidgetItem

from panda3d.core import loadPrcFileData
from PySide6.QtGui import QKeyEvent, QCloseEvent
from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import QApplication, QDialog

from gen.ui_modeldefault import Ui_ModelDefault


class ModelDefault(QDialog):
    content_updated = Signal()
    panda_win = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.model_dict = None
        self.ui = Ui_ModelDefault()
        self.ui.setupUi(self)
        self.setWindowTitle("模型默认值")

        # 使本控件可以响应键盘事件，详情参考：https://blog.csdn.net/zhujiangm/article/details/90760744
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

        # 设置Panda内嵌窗口大小(两个一起用，否则绘制区域不会跟着一起变)
        self.ui.defaultPandaWidget.setGeometry(527, 56, 505, 543)
        self.ui.defaultPandaWidget.setShowArea()

        # 设置panda3d自己的窗口界面不显示
        loadPrcFileData("", "window-type offscreen")
        loadPrcFileData("", f"win-size 505 543")

        # 设置Panda本身窗口大小
        self.panda_win = PandaHandler()

        # 设置Panda窗口内容映射到Qt窗口中
        render_widget = self.ui.defaultPandaWidget
        self.panda_widget = QtPandaWidget(render_widget, self.panda_win.screenTexture, self.panda_win.taskMgr.step)
        self.panda_widget.setGeometry(0, 0, render_widget.width(), render_widget.height())
        self.panda_widget.setShowArea()
        self.panda_widget.show()

    def closeEvent(self, event: QCloseEvent) -> None:
        self.panda_win.destroy()
        event.accept()

    def setModelInfo(self, model_dict: dict) -> None:
        self.model_dict = model_dict
        self.panda_win.setModel(model_dict)
        self.showJson()

    def showJson(self) -> None:
        self.ui.jsonTreeWidget.setJson(self.model_dict)
        self.ui.jsonTreeWidget.jsonChanged.connect(self.jsonContentChanged)
        self.ui.jsonTreeWidget.jsonChanged.connect(self.adjustModel)

    # 单元格内容修改后调用的槽函数

    @Slot(dict)
    def jsonContentChanged(self, changed_json: dict) -> None:
        # 修改json文件内容
        utils.modifyModelInfo(changed_json)
        self.content_updated.emit()

    @Slot(dict)
    def adjustModel(self, changed_json: dict) -> None:
        self.panda_win.adjustModel(changed_json)

    def closeEvent(self, event: QCloseEvent) -> None:
        print("close")
        if self.panda_widget is not None:
            self.close()
            self.panda_widget.timerStop()
            del self.panda_widget
            self.panda_widget = None
        if self.panda_win is not None:
            self.panda_win.destroy()
            self.panda_win = None
        self.close()

    # 键盘事件槽函数，debug用的
    # def keyPressEvent(self, event: QKeyEvent) -> None:
    #     pprint.pprint(event.key())
    #     pressed_key = event.key()
    #     if pressed_key == Qt.Key_R:
    #         self.panda_win.runTestModel()




if __name__ == "__main__":
    app = QApplication([])
    widget = ModelDefault()
    widget.show()
    app.exec()
