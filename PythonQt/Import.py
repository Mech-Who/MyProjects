import json
import os.path
import shutil

from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QDialog, QMessageBox, QFileDialog
from PySide6.QtGui import QPixmap

from gen.ui_importmodel import Ui_ImportModel
import utils


def model_import(file_path, file_format, icon_path, model_name) -> dict:
    """
    根据给定的模型文件导入json配置文件，并返回是否成功的布尔值
    :param: 要导入的模型文件的路径
    """
    # 将模型文件复制一份到模型文件夹中
    with open("config.json", "r", encoding="utf-8") as f:
        content = json.load(f)
    model_save_dir = content.get("model_save")
    file_name = os.path.split(file_path)[1]
    new_file_path = model_save_dir + file_name
    if not os.path.exists(new_file_path):
        shutil.copy(file_path, new_file_path)
    # 记录模型信息到dict中
    model_info = {
        "name": model_name,
        "type": file_format,
        "picBg": icon_path,
        "path": new_file_path,
        "accessories": {},
        "binding": {
            "Chest": {
                "func": {
                    "fx": "None",
                    "fy": "None",
                    "fz": "None"
                },
                "name": "None"
            },
            "Hips": {
                "func": {
                    "fx": "None",
                    "fy": "None",
                    "fz": "None"
                },
                "name": "None"
            },
            "LeftFoot": {
                "func": {
                    "fx": "None",
                    "fy": "None",
                    "fz": "None"
                },
                "name": "None"
            },
            "LeftHand": {
                "func": {
                    "fx": "None",
                    "fy": "None",
                    "fz": "None"
                },
                "name": "None"
            },
            "LeftLowerArm": {
                "func": {
                    "fx": "None",
                    "fy": "None",
                    "fz": "None"
                },
                "name": "None"
            },
            "LeftLowerLeg": {
                "func": {
                    "fx": "None",
                    "fy": "None",
                    "fz": "None"
                },
                "name": "None"
            },
            "LeftUpperArm": {
                "func": {
                    "fx": "None",
                    "fy": "None",
                    "fz": "None"
                },
                "name": "None"
            },
            "LeftUpperLeg": {
                "func": {
                    "fx": "None",
                    "fy": "None",
                    "fz": "None"
                },
                "name": "None"
            },
            "Neck": {
                "func": {
                    "fx": "None",
                    "fy": "None",
                    "fz": "None"
                },
                "name": "None"
            },
            "RightFoot": {
                "func": {
                    "fx": "None",
                    "fy": "None",
                    "fz": "None"
                },
                "name": "None"
            },
            "RightHand": {
                "func": {
                    "fx": "None",
                    "fy": "None",
                    "fz": "None"
                },
                "name": "None"
            },
            "RightLowerArm": {
                "func": {
                    "fx": "None",
                    "fy": "None",
                    "fz": "None"
                },
                "name": "None"
            },
            "RightLowerLeg": {
                "func": {
                    "fx": "None",
                    "fy": "None",
                    "fz": "None"
                },
                "name": "None"
            },
            "RightUpperArm": {
                "func": {
                    "fx": "None",
                    "fy": "None",
                    "fz": "None"
                },
                "name": "None"
            },
            "RightUpperLeg": {
                "func": {
                    "fx": "None",
                    "fy": "None",
                    "fz": "None"
                },
                "name": "None"
            },
            "Spine": {
                "func": {
                    "fx": "None",
                    "fy": "None",
                    "fz": "None"
                },
                "name": "None"
            },
        },
        "cameraPosition": {
            "x": 0.0,
            "y": 0.0,
            "z": 0.0
        },
        "cameraRotation": {
            "x": 0.0,
            "y": 0.0,
            "z": 0.0
        },
        "cameraTarget": {
            "x": 1.0,
            "y": 1.0,
            "z": 1.0
        },
        "init": {}
    }
    # 将模型信息写入json文件
    with open("models.json", "r", encoding="utf-8") as f:
        model_json = json.load(f)
    model_json["import_models"].append(model_info)
    model_json["import_model_count"] += 1
    with open("models.json", "w", encoding='utf-8') as f:
        # json.dump(dict_var, f)  # 写为一行
        json.dump(model_json, f, indent=2, sort_keys=True, ensure_ascii=False)  # 写为多行
    return model_info


class ImportModel(QDialog):
    modelImport = Signal(type({}))

    def __init__(self, parent=None):
        super().__init__(parent)
        # 类成员
        self.model_path = None
        # 设置界面魏我们生成的界面
        self.ui = Ui_ImportModel()
        self.ui.setupUi(self)
        # 初始化
        self.init_combobox()
        # 绑定信号与槽
        self.ui.cancelButton.clicked.connect(self.close)

    def init_combobox(self) -> None:
        """
        初始化comboBox中的所有选项
        """
        with open("./config.json", "r", encoding="utf-8") as f:
            content = json.load(f)
        self.ui.fileFormatComboBox.addItems(content.get("supported_format"))

    @Slot()
    def on_importButton_clicked(self):
        """
        importButton按钮的槽函数
        获取控件内容，并判断文件格式是否有误，无误则导入
        :return: 无
        """
        model_name = self.ui.modelNameLineEdit.text()
        file_format = self.ui.fileFormatComboBox.currentText()
        model_file = self.ui.modelFileLineEdit.text()
        icon_path = self.ui.imageFileLineEdit.text()
        if not utils.checkFileSuffix(file_format, model_file):
            QMessageBox.critical(self, "导入错误", "文件格式有误!")
            return True
        model_info = model_import(model_file, file_format, icon_path, model_name)
        self.modelImport.emit(model_info)
        self.close()

    @Slot()
    def on_fileSelectToolButton_clicked(self):
        """
        fileSelectToolButton按钮的槽函数
        打开文件选择窗，选择好之后将文件路径(含文件名)显示在modelFileLineEdit中
        """
        file_path = QFileDialog.getOpenFileName(self, "导入文件", "c:\\")
        # file_path格式: ('C:/filename.dll', 'All Files (*)')
        self.ui.modelFileLineEdit.setText(file_path[0])

    @Slot()
    def on_imageFileToolButton_clicked(self):
        """
        导入模型的展示图片
        """
        file_path = QFileDialog.getOpenFileName(self, "导入文件", "c:\\")
        # file_path格式: ('C:/filename.dll', 'All Files (*)')
        self.ui.imageFileLineEdit.setText(file_path[0])
        image_pixmap = QPixmap(file_path[0]).scaled(self.ui.imageLabel.width(), self.ui.imageLabel.height())
        self.ui.imageLabel.setPixmap(image_pixmap)
