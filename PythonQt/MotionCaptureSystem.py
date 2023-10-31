import os
import sys
import json
import panda3d
import pprint

import cv2
import mediapipe as mp
from PySide6.QtCore import QTimer, Slot, QSize
from PySide6.QtGui import QAction, QIcon, QCloseEvent, QPixmap
from PySide6.QtWidgets import QMainWindow, QFileDialog, QSystemTrayIcon, QMenu, QApplication, QMessageBox
import panda3d.core as pc
from panda3d.core import loadPrcFileData

# 导入界面ui文件生成的类
from gen.ui_mainwindow import Ui_MainWindow

# 导入自己的类
from ModelDefault import ModelDefault
from SkeletonMapping import SkeletonMapping
from Import import ImportModel
from QtPandaWidget import PandaHandler, QtPandaWidget
import utils


class MotionCaptureSystem(QMainWindow):
    """
    主界面
    """
    # 类成员
    default_model = None
    showing_model_dict = None
    tray_icon_menu = None
    tray_icon = None
    timer = None
    capture = None
    mp_holistic = None
    holistic = None
    mp_drawing = None
    mp_drawing_styles = None
    results = None
    panda_win = None

    def __init__(self, parent=None):
        super().__init__(parent)

        with open("config.json", "r", encoding="utf-8") as f:
            self.config = json.load(f)
        # 设置界面为我们生成的界面
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # 界面初始化
        self.setWindowTitle("MotionCaptureSystem")
        self.setWindowIcon(QIcon(os.path.join('assets/sys.png')))
        self.resize(1200, 700)
        self.initModels()
        self.initPall()
        # 绑定槽函数

    def __del__(self):
        if self.capture is not None:
            self.capture.release()

    def getConfig(self):
        return self.config

    def initPall(self) -> None:
        """
        配置软件的托盘化
        """
        # 导入准备在托盘化显示上使用的图标
        icons = os.path.join('assets/sys.png')

        # 设置右键显示最小化的菜单项
        # 菜单项退出，点击后调用quit函数
        quit_action = QAction('退出', self, triggered=self.quit)
        # 设置这个点击选项的图片
        quit_action.setIcon(QIcon(icons))
        # 菜单项显示，点击后调用showing函数
        showing = QAction(u'显示', self, triggered=self.showWindow)

        # 新建一个菜单项控件
        self.tray_icon_menu = QMenu(self)
        # 在菜单栏添加一个无子菜单的菜单项‘退出’和'显示'
        self.tray_icon_menu.addAction(quit_action)
        self.tray_icon_menu.addAction(showing)

        # QSystemTrayIcon类为应用程序在系统托盘中提供一个图标
        self.tray_icon = QSystemTrayIcon(self)
        # 设置托盘化图标
        self.tray_icon.setIcon(QIcon(icons))
        # 设置托盘化菜单项
        self.tray_icon.setContextMenu(self.tray_icon_menu)

        # 展示
        self.tray_icon.show()

    @Slot()
    def quit(self):
        """
        退出操作，关闭程序
        """
        self.close()
        sys.exit()

    @Slot()
    def showWindow(self):
        """
        显示窗体
        """
        # setWindowOpacity（）设置窗体的透明度，通过调整窗体透明度实现宠物的展示和隐藏
        # self.setWindowOpacity(1)
        self.show()

    def initModels(self) -> None:
        """
        列出所有系统中的模型和用户导入的模型
        """
        default_model = None
        with open("models.json", "r", encoding="utf-8") as f:
            content = json.load(f)
            self.default_model = content.get("system_models")[0]
        system_model_list = content.get("system_models")
        self.ui.systemModelListWidget.loadModels(system_model_list)
        self.ui.systemModelListWidget.item_clicked.connect(self.setModelInfo)
        self.ui.systemModelListWidget.item_double_clicked.connect(self.on_modelDefaultButton_clicked)
        import_model_list = content.get("import_models")
        self.ui.importModelListWidget.loadModels(import_model_list)
        self.ui.importModelListWidget.item_clicked.connect(self.setModelInfo)
        self.ui.importModelListWidget.item_double_clicked.connect(self.on_modelDefaultButton_clicked)
        # 设置默认模型信息
        self.showing_model_dict = self.default_model
        self.setModelInfo(self.default_model)

    def setModelInfo(self, model_dict: dict) -> None:
        """
        更新模型信息
        """
        if "id" in model_dict.keys():
            content = None
            if "isBuildIn" in model_dict and model_dict["isBuildIn"]:
                content = utils.getModelInfo(False)
            else:
                content = utils.getModelInfo(True)
            self.showing_model_dict = content[model_dict["id"]]
        else:
            self.showing_model_dict = model_dict
        img_path = model_dict["picBg"]
        utils.loadImageToLabel(self.ui.imageLabel, img_path)
        self.ui.modelInfoNameLineEdit.setText(model_dict["name"])
        self.ui.modelInfoNameLineEdit.setEnabled(False)
        self.ui.modelInfoFileLineEdit.setText(model_dict["path"])
        self.ui.modelInfoFileLineEdit.setEnabled(False)
        if "isBuildIn" in model_dict and model_dict["isBuildIn"]:
            self.ui.modelDeleteButton.setEnabled(False)
        else:
            self.ui.modelDeleteButton.setEnabled(True)

    def flushModelList(self):
        """
        刷新模型列表
        """
        print("list flushed!")
        sys_list = utils.getModelInfo(False)
        self.ui.systemModelListWidget.loadModels(sys_list)
        import_list = utils.getModelInfo(True)
        self.ui.systemModelListWidget.loadModels(sys_list)
        # self.ui.systemModelListWidget.flushModelList()
        # self.ui.importModelListWidget.flushModelList()

    # 模型导入槽函数

    @Slot()
    def on_actionImport_triggered(self):
        """
        点击导入菜单后，打开导入对话框
        """
        import_win = ImportModel(self)
        import_win.setWindowTitle("导入模型")
        import_win.modelImport.connect(self.ui.importModelListWidget.addModel)
        import_win.exec()

    # 视频预览槽函数

    def renderCameraInPanda3d(self, results):
        """
        渲染虚拟形象
        :param results: mediapipe的渲染结果
        """
        # 判断是否有pose_world_landmarks和pose_landmarks
        if results.pose_world_landmarks is None or results.pose_landmarks is None:
            print("No pose_world_landmarks or pose_landmarks")
            return
        # 处理results,获得坐标点,点类型使用的时panda3d提供的Point3
        pose_landmarks_3d = [lm for lm in results.pose_world_landmarks.landmark]
        pose_landmarks_2d = [lm for lm in results.pose_landmarks.landmark]
        self.panda_win.setSkeleton(pose_landmarks_3d, pose_landmarks_2d, self.ui.cameraWidget.fps)

    @Slot()
    def on_startPreviewButton_clicked(self):
        """
        startPreviewButton按钮的槽函数
        启动摄像头并开始渲染虚拟形象
        """
        print("on_startPreviewButton_clicked槽函数生效")
        # 设置摄像头画面
        if self.capture is None:
            self.capture = cv2.VideoCapture(0)
        else:
            self.capture.release()
            self.capture = cv2.VideoCapture(0)
        # 获取视频的帧数
        frame_count = 1466
        print(f"video frame count: {frame_count}")
        self.ui.cameraWidget.setFps(frame_count)
        render_widget = self.ui.renderCameraPandaWidget

        # 启动定时器
        # self.ui.renderCameraPandaWidget.timerStart()
        # 设置panda3d自己的窗口界面不显示
        loadPrcFileData("", "window-type offscreen")
        loadPrcFileData("", f"win-size 505 543")
        # 设置Panda本身窗口大小
        if self.panda_win is not None:
            self.panda_win.destroy()
        self.panda_win = PandaHandler()
        # 设置Panda窗口内容映射到Qt窗口中
        self.panda_widget = QtPandaWidget(render_widget, self.panda_win.screenTexture, self.panda_win.taskMgr.step)
        self.panda_widget.setGeometry(0, 0, render_widget.width(), render_widget.height())
        self.panda_widget.setShowArea()
        self.panda_widget.show()
        self.panda_widget.setFps(frame_count)
        # 设置Model
        self.panda_win.setModel(self.showing_model_dict)

        # 2.设置视频窗口
        # 启动视频播放
        self.ui.cameraWidget.setEnhanceParams(0.8, 50)
        self.ui.cameraWidget.setFlags(isEnhance=True, isMediaPipe=True, isMediaPipeDrawing=True)
        self.ui.cameraWidget.mediapipeProcess.connect(self.renderCameraInPanda3d)
        self.ui.cameraWidget.start_camera(self.capture)

    @Slot()
    def on_stopPreviewButton_clicked(self):
        """
        stopPreviewButton按钮的槽函数
        停止摄像头并停止渲染虚拟形象
        """
        self.ui.cameraWidget.stop_camera()
        self.panda_widget.timerStop()
        del self.panda_widget
        self.panda_win.destroy()
        del self.panda_win

    # 视频转换槽函数

    @Slot()
    def on_fileSelectToolButton_clicked(self):
        """
        fileSelectToolButton按钮的槽函数
        打开文件选择窗，选择好之后将文件路径(含文件名)显示在videoFileLineEdit中
        """
        file_path, file_type = QFileDialog.getOpenFileName(self, "选择视频", "c:\\")
        self.ui.videoFileLineEdit.setText(file_path)

    def renderVideoInPanda3d(self, results):
        """
        渲染虚拟形象
        :param results: mediapipe的渲染结果
        """
        # 判断是否有pose_world_landmarks和pose_landmarks
        if results.pose_world_landmarks is None or results.pose_landmarks is None:
            print("No pose_world_landmarks or pose_landmarks")
            return
        # 处理results,获得坐标点,点类型使用的时panda3d提供的Point3
        pose_landmarks_3d = [lm for lm in results.pose_world_landmarks.landmark]
        pose_landmarks_2d = [lm for lm in results.pose_landmarks.landmark]
        self.panda_win.setSkeleton(pose_landmarks_3d, pose_landmarks_2d, self.ui.videoWidget.fps)

    @Slot()
    def on_startVideoRenderButton_clicked(self):
        """
        startVideoRenderButton按钮的槽函数
        开始渲染视频
        """
        print("on_startVideoRenderButton_clicked槽函数生效")
        # 根据视频文件，设置OpenCV的VideoCapture
        video_path = self.ui.videoFileLineEdit.text()
        if video_path == "" or video_path is None:
            QMessageBox.critical(self, "错误", "请先选择视频文件！")
            return
        if self.capture is None:
            self.capture = cv2.VideoCapture(video_path)
        else:
            self.capture.release()
            self.capture = cv2.VideoCapture(video_path)
        # 获取视频的帧数
        frame_count = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
        print(f"video frame count: {frame_count}")
        self.ui.videoWidget.setFps(frame_count)
        render_widget = self.ui.renderVideoPandaWidget

        # 1.设置渲染窗口
        # 启动定时器
        # self.ui.renderVideoPandaWidget.timerStart()
        # 设置panda3d自己的窗口界面不显示
        loadPrcFileData("", "window-type offscreen")
        loadPrcFileData("", f"win-size 505 543")
        # 设置Panda本身窗口大小
        if self.panda_win is not None:
            self.panda_win.destroy()
        self.panda_win = PandaHandler()
        # 设置Panda窗口内容映射到Qt窗口中
        self.panda_widget = QtPandaWidget(render_widget, self.panda_win.screenTexture, self.panda_win.taskMgr.step)
        self.panda_widget.setGeometry(0, 0, render_widget.width(), render_widget.height())
        self.panda_widget.setShowArea()
        self.panda_widget.show()
        self.panda_widget.setFps(frame_count)
        # 设置Model
        self.panda_win.setModel(self.showing_model_dict)

        # 2.设置视频窗口
        # 启动视频播放
        self.ui.videoWidget.setEnhanceParams(0.8, 50)
        self.ui.videoWidget.setFlags(isEnhance=True, isMediaPipe=True, isMediaPipeDrawing=True)
        self.ui.videoWidget.mediapipeProcess.connect(self.renderVideoInPanda3d)
        self.ui.videoWidget.start_camera(self.capture)

    @Slot()
    def on_stopVideoRenderButton_clicked(self):
        """
        stopVideoRenderButton按钮的槽函数
        停止渲染视频
        """
        print("on_stopVideoRenderButton_clicked槽函数生效")
        self.ui.videoWidget.stop_camera()
        self.panda_widget.timerStop()
        del self.panda_widget
        self.panda_win.destroy()
        del self.panda_win

    # 模型管理槽函数

    @Slot()
    @Slot(dict)
    def on_modelDefaultButton_clicked(self, model_dict=None):
        """
        modelDefaultButton按钮的槽函数
        打开当前模型默认设置界面
        """
        model_default_win = ModelDefault(self)
        model_default_win.content_updated.connect(self.flushModelList)
        # model_default_win.content_updated.connect(self.infoUpdate)
        if model_dict is not None:
            model_default_win.setModelInfo(model_dict)
        else:
            model_default_win.setModelInfo(self.showing_model_dict)
        model_default_win.show()

    @Slot()
    def on_modelDeleteButton_clicked(self):
        """
        deleteModelButton按钮的槽函数
        删除当前模型
        """
        print("on_deleteModelButton_clicked槽函数生效")
        print("deleting model!")
        with open("./models.json", "r", encoding="utf-8") as f:
            full_models = json.load(f)
        full_models["import_model_count"] -= 1
        import_models = full_models["import_models"]
        for model in import_models:
            if model["path"] == self.showing_model_dict["path"]:
                import_models.remove(model)
                break
        with open("./models.json", "w", encoding="utf-8") as f:
            json.dump(full_models, f, ensure_ascii=False)
        # 刷新界面
        self.ui.importModelListWidget.deleteModel(self.showing_model_dict)
        # 设置默认显示模型
        self.showing_model_dict = self.default_model
        self.setModelInfo(self.default_model)
        print("delete success!")

    @Slot()
    @Slot(dict)
    def on_skeletonBindButton_clicked(self, model_dict=None):
        """
        modelBindButton按钮的槽函数
        打开骨骼绑定界面
        """
        model_bind_win = SkeletonMapping(self)
        if model_dict is not None:
            model_bind_win.setModelInfo(model_dict)
        else:
            model_bind_win.setModelInfo(self.showing_model_dict)
        model_bind_win.content_update.connect(self.flushModelList)
        # model_bind_win.content_update.connect(self.infoUpdate)
        model_bind_win.show()

    @Slot(dict)
    def infoUpdate(self, new_model_dict):
        print("model info updated!")
        # pprint.pprint(new_model_dict)
        self.showing_model_dict = new_model_dict
        if "isBuildIn" in new_model_dict and new_model_dict["isBuildIn"]:
            self.ui.systemModelListWidget.flushModelList()
        else:
            self.ui.importModelListWidget.flushModelList()

    # 窗口关闭槽函数

    @Slot(QCloseEvent)
    def closeEvent(self, event: QCloseEvent) -> None:
        # TODO:弹出弹窗让用户选择时直接退出还是最小化到托盘
        if self.getConfig().get("default_close"):
            self.close()
        else:
            self.hide()
            event.ignore()
