from PySide6.QtCore import QFileInfo, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QMessageBox
import win32gui
import win32con
import json

from kalidokit4python.Util.Vector import Vector
from kalidokit4python.Util import Vector as Vec


def checkFileSuffix(file_format, file_path) -> bool:
    """
    检查文件格式，相符返回True，否则返回False
    """
    file_info = QFileInfo(file_path)
    return str(file_format).lower() == str(file_info.suffix()).lower()


def embeddedOpencvWindow(window_name: str, control: QWidget) -> None:
    hWnd = win32gui.FindWindow(None, window_name)
    if hWnd is not None:
        win32gui.SetParent(hWnd, control.winId())
        # 获取指定窗口的有关信息，内存位置
        ptr = win32gui.GetWindowLong(hWnd, win32con.GWL_STYLE)
        # 指定偏移位置
        win32gui.SetWindowLong(hWnd, win32con.GWL_STYLE, ptr & (~win32con.WS_CAPTION))
        # 移动窗体
        win32gui.MoveWindow(hWnd, 0, 0, control.width(), control.height(), True)


def loadImageToLabel(label, image_path):
    """
    将图片加载到label中
    :param label: 要加载图片的label
    :param image_path: 图片路径
    :return:
    """
    label.setScaledContents(True)
    label.setAlignment(Qt.AlignCenter)
    window_size = label.size()
    pixmap = QPixmap(image_path)
    # 将图像缩放以适应窗口大小
    scaled_pixmap = pixmap.scaled(window_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    label.setPixmap(scaled_pixmap)


def modifyModelInfo(model_dict: dict, json_file: str = "./models.json") -> None:
    with open(json_file, "r", encoding="utf-8") as f:
        full_dict = json.load(f)
    model_type = None
    if "isBuildIn" in model_dict and model_dict["isBuildIn"]:
        model_type = "system_models"
    else:
        model_type = "import_models"
    models = full_dict[model_type]
    for i, m in enumerate(models):
        if m["path"] == model_dict["path"]:
            models[i] = model_dict
            break
    full_dict[model_type] = models
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(full_dict, f, indent=2, sort_keys=True, ensure_ascii=False)  # 写为多行


def getModelInfo(isImport=None):
    with open("./models.json", "r", encoding="utf-8") as f:
        content = json.load(f)
    if isImport is None:
        return content
    elif isImport:
        return content["import_models"]
    else:
        return content["system_models"]


def add(a: list, b: list, n: int = 3):
    new_list = []
    for i in range(n):
        new_list.append(a[i] + b[i])
    return new_list


def divide(a: list, b: int):
    new_list = []
    for i in range(len(a)):
        new_list.append(a[i] / b)
    return new_list

def center(a, b, n:int = 3):
    if isinstance(a, Vector):
        return Vec.divide(Vec.add(a, b), 2)
    elif isinstance(a, list):
        new_list = []
        for i in range(n):
            new_list.append((a[i] + b[i]) / 2)
        return new_list
    else:
        x = (a.x + b.x) / 2
        y = (a.y + b.y) / 2
        z = (a.z + b.z) / 2
        return Vector(x, y, z)


def calculate_coords(pose_coords):
    """
    基于Mediapipe骨骼模型，再计算额外的关键点坐标，主要是人体脊椎的几个点。
    额外点分别基座ABCDE点，从上往下依次排列，C是AE中点，B和D分别是AC和CE的中点
    """
    # 计算额外点，并添加额外点到pose_coords中，A-E分别对应33-37
    if len(pose_coords) < 25:
        print("pose_coords长度不够，无法计算额外点坐标")
        return pose_coords
    coord_A = center(pose_coords[9], pose_coords[10])
    pose_coords.append(coord_A)
    coord_B = center(pose_coords[12], pose_coords[11])
    pose_coords.append(coord_B)
    coord_E = center(pose_coords[23], pose_coords[24])
    coord_mid = center(coord_B, coord_E)
    coord_C = center(coord_B, coord_mid)
    pose_coords.append(coord_C)
    coord_D = center(coord_mid, coord_E)
    pose_coords.append(coord_D)
    pose_coords.append(coord_E)
    return pose_coords


class File(object):

    # 初始化方法
    def __init__(self, widget, file_name, file_model, encoding="utf-8"):
        # 定义变量保存文件名和打开模式
        self.widget = widget
        self.file_name = file_name
        self.file_model = file_model
        self.encoding = encoding

    # 上文方法
    def __enter__(self):
        try:
            # 返回文件资源
            self.file = open(self.file_name, self.file_model, encoding=self.encoding)
        # 捕获的异常可能不全面
        except IOError:
            QMessageBox.critical(self.widget, "文件操作错误", "文件操作失败！")
        return self.file

    # 下文方法
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
