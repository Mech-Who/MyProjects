import cv2
import mediapipe as mp
from collections import namedtuple
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QSizePolicy


class LabelCVWidget(QWidget):
    # 定义信号
    mediapipeProcess = Signal(object)

    # 声明变量
    alpha = 1
    beta = 0
    mp_holistic = None
    holistic = None
    mp_drawing = None
    mp_drawing_styles = None
    isMediaPipe = False
    isMediaPipeDrawing = False
    isEnhance = False
    fps = 30
    results = None
    capture = None

    def __init__(self, parent=None):
        super().__init__(parent)

        # 窗口初始化
        self.setWindowTitle("OpenCV Viewer")

        # 准备调用Mediapipe
        self.init_mediapipe()

        # 创建 QLabel 用于显示图像
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setContentsMargins(0, 0, 0, 0)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 创建垂直布局并将 QLabel 添加到布局中
        layout = QVBoxLayout(self)
        layout.addWidget(self.image_label)

        # 定时器用于更新图像
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_image)

    def __del__(self):
        if self.capture is not None:
            self.capture.release()

    def setFps(self, fps):
        self.fps = fps

    def setFlags(self, isEnhance=False, isMediaPipe=False, isMediaPipeDrawing=False):
        self.isEnhance = isEnhance
        self.isMediaPipe = isMediaPipe
        self.isMediaPipeDrawing = isMediaPipeDrawing

    def start_camera(self, capture=None):
        # 打开摄像头
        if capture is None:
            self.capture = cv2.VideoCapture(0)
        else:
            self.capture = capture
        # 打开计时器,帧率为self.fps
        self.timer.start(int(1000 / self.fps))

    def stop_camera(self):
        if self.timer.isActive():
            # 停止定时器
            self.timer.stop()
        if self.capture is not None:
            # 释放摄像头
            self.capture.release()

    def setEnhanceParams(self, alpha=1, beta=0):
        self.alpha = alpha
        self.beta = beta

    def setImageEnhance(self, frame):
        frame = cv2.convertScaleAbs(frame, alpha=self.alpha, beta=self.beta)  # 调整对比度和亮度
        frame = cv2.medianBlur(frame, 3)  # 画面平滑
        return frame

    def init_mediapipe(self) -> None:
        """
        初始化mediapipe的holistic算法的配置
        """
        self.mp_holistic = mp.solutions.holistic
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.holistic = self.mp_holistic.Holistic(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            # enable_segmentation=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def setMediaPipeProcess(self, frame):
        self.results = self.holistic.process(frame)
        self.mediapipeProcess.emit(self.results)
        return self.results

    def setMediaPipeDrawing(self, frame):
        # 绘制人脸关键点
        self.mp_drawing.draw_landmarks(
            frame,
            self.results.face_landmarks,
            self.mp_holistic.FACEMESH_CONTOURS,
            landmark_drawing_spec=self.mp_drawing.DrawingSpec(color=(0,0,255),thickness=2,circle_radius=2),
            connection_drawing_spec=self.mp_drawing_styles
            .get_default_face_mesh_contours_style())
        # 绘制人体关键点
        self.mp_drawing.draw_landmarks(
            frame,
            self.results.pose_landmarks,
            self.mp_holistic.POSE_CONNECTIONS,
            landmark_drawing_spec=self.mp_drawing_styles
            .get_default_pose_landmarks_style())
        # 绘制左手关键点
        self.mp_drawing.draw_landmarks(
            frame,
            self.results.left_hand_landmarks,
            self.mp_holistic.HAND_CONNECTIONS,
            landmark_drawing_spec=self.mp_drawing_styles
            .get_default_pose_landmarks_style())
        # 绘制右手关键点
        self.mp_drawing.draw_landmarks(
            frame,
            self.results.right_hand_landmarks,
            self.mp_holistic.HAND_CONNECTIONS,
            landmark_drawing_spec=self.mp_drawing_styles
            .get_default_pose_landmarks_style())
        return frame

    def getMediaPipeProcessResult(self):
        return self.results

    def update_image(self):
        # 从摄像头捕获图像（示例）
        ret, frame = self.capture.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if self.isEnhance:
                frame = self.setImageEnhance(frame)
            if self.isMediaPipe:
                results = self.setMediaPipeProcess(frame)
            if self.isMediaPipeDrawing:
                frame = self.setMediaPipeDrawing(frame)

            # 将 OpenCV 图像转换为 Qt 图像
            h, w, _ = frame.shape
            qt_image = QImage(frame.data, w, h, QImage.Format_RGB888)

            # 创建缩放后的图像
            pixmap = QPixmap.fromImage(qt_image)
            scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio)

            # 在 QLabel 中显示缩放后的图像
            self.image_label.setPixmap(scaled_pixmap)


if __name__ == "__main__":
    app = QApplication([])
    window = LabelCVWidget()
    capture = cv2.VideoCapture(r"D:\Task\Projects\Myself\GraduationDesign\PythonQt\assets\video\dance.mp4")
    window.start_camera(capture)
    window.show()
    app.exec()
