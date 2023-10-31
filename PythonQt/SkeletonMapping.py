# This Python file uses the following encoding: utf-8
# 标准库
import json
import pprint
import os

from PySide6.QtCore import Signal
from PySide6.QtGui import QCloseEvent

# 自己的库
import utils
# 第三方库
# panda3d
import panda3d.core as pc
from direct.actor.Actor import Actor
from direct.showbase.ShowBase import ShowBase
# PySide6
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QDialog, QTableWidgetItem, QTreeWidgetItem, QMessageBox
# 生成的ui文件
from gen.ui_skeletonmap import Ui_SkeletonMapping


class SkeletonMapping(QDialog):
    skeleton_list = ["Neck", "Chest", "Spine", "Hips", "LeftUpperLeg", "LeftLowerLeg", "RightUpperLeg",
                     "RightLowerLeg", "LeftFoot", "RightFoot", "LeftUpperArm", "LeftLowerArm", "RightUpperArm",
                     "RightLowerArm", "LeftHand", "RightHand"]
    model = None
    joints = []
    model_json_file = "./models.json"

    content_update = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_SkeletonMapping()
        self.ui.setupUi(self)
        self.setWindowTitle("骨骼绑定")

        self.ui.middleSkeletonTableWidget.setColumnCount(4)
        self.ui.middleSkeletonTableWidget.setRowCount(len(self.skeleton_list))
        self.ui.middleSkeletonTableWidget.setHorizontalHeaderLabels(["模型绑定骨骼", "fx", "fy", "fz"])
        self.ui.middleSkeletonTableWidget.setVerticalHeaderLabels(self.skeleton_list)
        self.ui.middleSkeletonTableWidget.itemChanged.connect(self.handleItemChanged)

    def setModelInfo(self, model_info):
        self.model_dict = model_info
        self.showBinding()
        self.showModelSkeleton()

    def showBinding(self) -> None:
        model_binding = self.model_dict["binding"]
        for id, bone in enumerate(self.skeleton_list):
            if bone in model_binding.keys():
                self.ui.middleSkeletonTableWidget.setItem(id, 0, QTableWidgetItem(model_binding[bone]["name"]))
                self.ui.middleSkeletonTableWidget.setItem(id, 1, QTableWidgetItem(model_binding[bone]["func"]["fx"]))
                self.ui.middleSkeletonTableWidget.setItem(id, 2, QTableWidgetItem(model_binding[bone]["func"]["fy"]))
                self.ui.middleSkeletonTableWidget.setItem(id, 3, QTableWidgetItem(model_binding[bone]["func"]["fz"]))

    def showModelSkeleton(self):
        # 获得模型
        panda_case = ShowBase()
        model_path = self.model_dict["path"]
        model_file = pc.Filename.from_os_specific(os.path.abspath(model_path))
        model_root = panda_case.loader.loadModel(model_file)
        panda_case.destroy()
        self.model = Actor(model_root)
        # 获得模型骨骼
        current_joint = self.model.getJoints()[0]
        self.joints = [current_joint]
        top_item = QTreeWidgetItem()
        top_item.setText(0, current_joint.getName())
        items = [top_item]
        current_item = top_item
        once = True
        while True:
            current_joint = self.joints.pop()
            current_item = items.pop()
            for joint in current_joint.getChildren():
                self.joints.append(joint)
                joint_item = QTreeWidgetItem()
                joint_item.setText(0, joint.getName())
                items.append(joint_item)
                current_item.addChild(joint_item)
            if len(items) == 0:
                break
        # 添加骨骼到树形控件
        self.ui.modelSkeletonTreeWidget.addTopLevelItem(top_item)

    @QtCore.Slot()
    def handleItemChanged(self, item: QTableWidgetItem) -> None:
        # print("handleItemChanged")
        # pprint.pprint(item)
        row = item.row()
        column = item.column()
        # 修改model_dict内容
        key = self.skeleton_list[row]

        value = item.text().strip()
        if column == 0 and value == "":
            return
        model_binding = self.model_dict["binding"]
        if column == 0:
            model_binding[key]["name"] = value
        elif column == 1:
            if value == "":
                value = "x"
            model_binding[key]["func"]["fx"] = value
        elif column == 2:
            if value == "":
                value = "-z"
            model_binding[key]["func"]["fy"] = value
        elif column == 3:
            if value == "":
                value = "y"
            model_binding[key]["func"]["fz"] = value
        # 修改json文件内容
        utils.modifyModelInfo(self.model_dict, self.model_json_file)

    @QtCore.Slot()
    def on_bindButton_clicked(self):
        """
        绑定按钮实现功能
        :return:
        """
        # print("on_bindButton_cilcked槽函数生效")
        table_item = self.ui.middleSkeletonTableWidget.selectedItems()
        tree_item = self.ui.modelSkeletonTreeWidget.selectedItems()
        # 错误提醒
        if len(table_item) == 0:
            QMessageBox.critical(self, "错误", "请选择要绑定的中间骨骼!")
            return
        elif len(table_item) > 1:
            QMessageBox.critical(self, "错误", "只能选择一个中间骨骼!")
            return
        if len(tree_item) == 0:
            QMessageBox.critical(self, "错误", "请选择要绑定的模型骨骼!")
            return
        elif len(tree_item) > 1:
            QMessageBox.critical(self, "错误", "只能选择一个模型骨骼!")
            return
        # 设置绑定内容
        table_item = table_item[0]
        row = table_item.row()
        tree_item = tree_item[0]
        model_bone = tree_item.text(0)
        self.ui.middleSkeletonTableWidget.item(row, 0).setText(model_bone)
        self.ui.middleSkeletonTableWidget.item(row, 1).setText("x")
        self.ui.middleSkeletonTableWidget.item(row, 2).setText("-z")
        self.ui.middleSkeletonTableWidget.item(row, 3).setText("y")
        # 主动调用文件保存函数
        self.handleItemChanged(table_item)

    def closeEvent(self, event: QCloseEvent) -> None:
        model_binding = self.model_dict["binding"]
        total_row = self.ui.middleSkeletonTableWidget.rowCount()
        for i in range(total_row):
            item0 = self.ui.middleSkeletonTableWidget.item(i, 0)
            item1 = self.ui.middleSkeletonTableWidget.item(i, 1)
            item2 = self.ui.middleSkeletonTableWidget.item(i, 2)
            item3 = self.ui.middleSkeletonTableWidget.item(i, 3)
            name = item0.text()
            fx = item1.text()
            fy = item2.text()
            fz = item3.text()
            sk_name = self.skeleton_list[i]
            model_binding[sk_name]['name'] = name
            model_binding[sk_name]['func']['fx'] = fx
            model_binding[sk_name]['func']['fy'] = fy
            model_binding[sk_name]['func']['fz'] = fz
        self.model_dict["binding"] = model_binding
        utils.modifyModelInfo(self.model_dict, self.model_json_file)
        self.content_update.emit(self.model_dict)
        self.close()



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = SkeletonMapping()
    model_d = {}
    with open("models.json", "r", encoding="utf-8") as f:
        model_d = json.load(f)["system_models"][-1]
    widget.setModelInfo(model_d)
    widget.show()
    app.exec()
