from PySide6.QtWidgets import QWidget

# -*- coding: utf-8 -*-
import time
import os

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QCursor, QPixmap, QMouseEvent
from PySide6.QtWidgets import QApplication, QMenu, QAbstractItemView, QListWidgetItem
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QListView


class ModelListWidget(QtWidgets.QListWidget):
    # signal = Signal(list)
    item_clicked = Signal(type({}))
    item_double_clicked = Signal(type({}))

    model_info_list = []
    grid_width = 90
    grid_height = 120
    interval = 50

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('All Images')
        self.resize(1400, 700)

        # 设置每个item size
        self.setGridSize(QtCore.QSize(self.grid_height + self.interval, self.grid_width + self.interval))
        # 设置横向list
        self.setFlow(QListView.LeftToRight)
        # 设置换行
        self.setWrapping(True)
        # 窗口size 变化后重新计算列数
        self.setResizeMode(QtWidgets.QListView.Adjust)
        # 设置选择模式
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setIconSize(QSize(self.grid_height, self.grid_width))

    def mouseDoubleClickEvent(self, e: QMouseEvent) -> None:
        """
        处理鼠标双击事件
        :param e: 鼠标事件
        :return:
        """
        super().mouseDoubleClickEvent(e)
        selected = self.selectedItems()
        for item in selected:
            model_dict = item.model_dict
            print("double clicked: ", model_dict)
            self.item_double_clicked.emit(model_dict)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        处理鼠标点击事件
        :param event: 鼠标事件
        :return:
        """
        super().mousePressEvent(event)
        selected = self.selectedItems()
        for item in selected:
            model_dict = item.model_dict
            print("clicked: ", model_dict)
            self.item_clicked.emit(model_dict)

    def flushModelList(self):
        self.clear()
        self.loadModels(self.model_info_list)

    def loadModel(self, model_dict) -> None:
        """
        加载单个模型
        :param model_dict: 包含模型信息的字典
        :return:
        """
        model_item = ModelQListWidgetItem(model_dict)
        self.addItem(model_item)
        self.setItemWidget(model_item, model_item.widget)
        # 刷新界面
        QApplication.processEvents()

    def loadModels(self, model_info_list) -> None:
        """
        批量加载模型
        :param model_info_list: 模型信息列表
        :return:
        """
        self.model_info_list = model_info_list
        for index, model in enumerate(model_info_list):
            model["id"] = index
            self.loadModel(model)

    def addModel(self, model_dict) -> None:
        """
        添加模型
        :param model_dict: 模型信息字典
        :return:
        """
        self.model_info_list.append(model_dict)
        self.loadModel(model_dict)
        # 刷新界面
        QApplication.processEvents()

    def deleteModel(self, model_dict) -> None:
        """
        删除模型
        :param model_dict: 模型信息字典
        :return:
        """
        self.model_info_list.remove(model_dict)
        for i in range(self.count()):
            item = self.item(i)
            if item.model_dict == model_dict:
                self.takeItem(i)
                break
        # 刷新界面
        QApplication.processEvents()


# 自定义的item 继承自QListWidgetItem
class ModelQListWidgetItem(QListWidgetItem):
    def __init__(self, model_dict, target_width=90, target_height=120):
        super().__init__()

        self.model_info = model_dict
        # for test
        img_path = model_dict.get("picBg")
        # img_path = model_dict.get("picBg")
        # 自定义item中的widget 用来显示自定义的内容
        self.widget = QWidget()
        # 用来显示name
        self.nameLabel = QLabel()
        self.nameLabel.setText(model_dict.get("name"))
        # 用来显示avator(图像)
        self.avatorLabel = QLabel()
        # 设置图像源 和 图像大小
        img_obg = QPixmap(img_path)
        width = img_obg.width()
        height = img_obg.height()
        if width < height:
            scale_size = QSize(target_width, target_height)
        else:
            scale_size = QSize(target_height, target_width)
        self.avatorLabel.setPixmap(QPixmap(img_path).scaled(scale_size))
        # 图像自适应窗口大小
        self.avatorLabel.setScaledContents(True)
        # 设置布局用来对nameLabel和avatorLabel进行布局
        self.hbox = QVBoxLayout()
        self.hbox.addWidget(self.avatorLabel)
        self.hbox.addWidget(self.nameLabel)
        self.hbox.addStretch(1)
        # 设置widget的布局
        self.widget.setLayout(self.hbox)
        # 设置自定义的QListWidgetItem的sizeHint，不然无法显示
        self.setSizeHint(self.widget.sizeHint())

    @property
    def model_dict(self) -> dict:
        return self.model_info


import json

if __name__ == '__main__':
    print('main layout show')
    now = time.time()
    app = QApplication([])
    main_window = ModelListWidget()
    main_window.show()

    with open("models.json", "r", encoding="utf-8") as f:
        content = json.load(f)
    model_list = content.get("system_models")
    main_window.loadModels(model_list)

    # 绑定点击槽函数 点击显示对应item中的name
    main_window.itemClicked.connect(lambda item: print('clicked item label:', item.nameLabel.text()))
    print("ImageListWidget 耗时: {:.2f}秒".format(time.time() - now))

    app.exec()
