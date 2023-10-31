import math
import os
import sys

from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QWidget, QLabel
from direct.interval.LerpInterval import LerpHprInterval
from direct.interval.MetaInterval import Parallel
from direct.showbase.ShowBase import ShowBase
from direct.task.TaskManagerGlobal import taskMgr
from direct.actor.Actor import Actor
import panda3d.core as pc
from panda3d.core import loadPrcFileData, Point3, GraphicsOutput, Texture, StringStream, PNMImage

from kalidokit4python.Pose.PoseSolver import PoseSolver
from kalidokit4python.Util.Vector import Vector


class QtPandaWidget(QWidget):
    """
    This takes a texture from Panda and draws it as a QWidget
    """
    fps = 30

    def __init__(self, parent=None, texture=None, panda_taskmgr_step=None):
        QWidget.__init__(self, parent)

        self.setWindowTitle("PandaQt")
        self.pandaTexture = texture

        # Set up a timer in Qt that runs taskMgr.step() to simulate Panda's own main loop
        self.pandaTimer = QTimer(self)
        self.pandaTimer.timeout.connect(panda_taskmgr_step)
        # self.pandaTimer.timeout.connect(self.panda_timeout_emit)
        # self.pandaTimer.start(1000 / self.fps)

        # Set up another timer that redraws this widget in a specific FPS
        self.redrawTimer = QTimer(self)
        self.redrawTimer.timeout.connect(self.update)
        # self.redrawTimer.timeout.connect(self.redraw_timeout_emit)
        self.timerStart()

        # Set up a QLabel to paint the pixmap on
        self.paintSurface = QLabel(self)
        self.paintSurface.setGeometry(0, 0, self.width(), self.height())
        self.paintSurface.show()
        self.paintPixmap = QPixmap(self.width(), self.height())

    def panda_timeout_emit(self):
        print("panda!")

    def redraw_timeout_emit(self):
        print("redraw!")

    def timerStart(self):
        self.pandaTimer.start(1000 / self.fps)
        self.redrawTimer.start(1000 / self.fps)

    def timerStop(self):
        self.pandaTimer.stop()
        self.redrawTimer.stop()

    def setShowArea(self):
        # Set up a QLabel to paint the pixmap on
        self.paintSurface = QLabel(self)
        self.paintSurface.setGeometry(0, 0, self.width(), self.height())
        self.paintSurface.show()
        self.paintPixmap = QPixmap(self.width(), self.height())

    def setTexture(self, texture):
        self.pandaTexture = texture

    def resetTexture(self):
        self.pandaTexture = None

    # Use the paint event to pull the contents of the panda texture to the widget
    def paintEvent(self, event):
        screenData = StringStream()  # Used to pass the data as a string
        screenImage = PNMImage()  # Converts the texture data into a format usable with Qt

        if (self.pandaTexture is not None) and self.pandaTexture.hasRamImage():
            self.pandaTexture.store(screenImage)
            screenImage.write(screenData, "win.ppm")
            self.paintPixmap.loadFromData(screenData.getData())
            self.paintSurface.setPixmap(self.paintPixmap)

    def setFps(self, fps):
        self.fps = fps

    def close(self) -> bool:
        self.timerStop()
        return super().close()


class PandaHandler(ShowBase):
    model_dict = {}
    model = None
    actor = None

    factor = 1

    standard_position = None
    standard_rotation = None
    standard_scale = None

    position_offset = {
        "x": 0,
        "y": 0,
        "z": 30
    }

    skeleton = {}
    skeleton_map = {}
    skeleton_key = {
            "Neck": [33, 34],
            "Chest": [34, 35],
            "Spine": [35, 36],
            "Hips": [36, 37],
            "LeftUpperLeg": [23, 25],
            "LeftLowerLeg": [25, 27],
            "RightUpperLeg": [24, 26],
            "RightLowerLeg": [26, 28],
            "LeftFoot": [27, 31],
            "RightFoot": [28, 32],
            "LeftUpperArm": [11, 13],
            "LeftLowerArm": [13, 15],
            "RightUpperArm": [12, 14],
            "RightLowerArm": [14, 16],
            "LeftHand": [15, 19],
            "RightHand": [16, 20]
        }

    init_rotation = {}
    init_position = {}

    parallel_interval = Parallel()

    def __init__(self):
        ShowBase.__init__(self)
        self.screenTexture = Texture()
        self.screenTexture.setMinfilter(Texture.FTLinear)
        self.win.addRenderTexture(self.screenTexture, GraphicsOutput.RTMCopyRam)
        loadPrcFileData("", "notify-level error")

    def destroy(self):
        self.parallel_interval.finish()
        for key in self.skeleton.keys():
            self.actor.releaseJoint("modelRoot", self.skeleton_map[key])
        super().destroy()

    def setModel(self, model_dict: dict):
        model_file = pc.Filename.from_os_specific(os.path.abspath(model_dict["path"]))
        self.model_dict = model_dict
        self.model = self.loader.loadModel(model_file)

        # 封装为Actor
        self.actor = Actor(self.model)
        self.actor.reparentTo(self.render)

        # 初步调整模型大小和位置
        bounds = self.actor.getTightBounds()

        center = bounds[0] + ((bounds[1] - bounds[0]) / 2.0)
        radius = (bounds[1] - center).length()
        scale = 0.5 * radius
        self.actor.setScale(scale)
        self.actor.setPos(0, 0, 0)

        self.standard_position = self.actor.getPos()
        self.standard_rotation = self.actor.getHpr()
        self.standard_scale = scale

        # 调整摄像机位置和朝向
        cam_distance = 2 * radius
        self.camera.setPos(0, -cam_distance, 0)
        self.camera.lookAt(self.actor.getPos())

        # 根据设置二次微调模型
        self.adjustModel(model_dict)

        # 设置骨骼映射表
        self.skeleton_map = {k: v["name"] for k, v in model_dict["binding"].items()}

    def adjustModel(self, model_dict: dict):
        # 根据cameraPosition、cameraRotation、cameraTarget调整摄像头中模型的位置、旋转和缩放
        position = model_dict["cameraPosition"]
        rotation = model_dict["cameraRotation"]
        scale = model_dict["cameraTarget"]

        # position
        self.actor.setPos(self.standard_position + Point3(*position.values()))
        # rotation
        self.actor.setHpr(self.standard_rotation + Point3(*rotation.values()))
        # scale
        self.actor.setScale(self.standard_scale * min(*scale.values()))

    def draw_reference_coord(self, pose_coords, factor=10, offset=10, with_line=True):
        """
        绘制基于关键点的参考模型
        """
        # 绘制关键点位置
        box = self.loader.loadModel("models/box")
        box.setScale(0.05)
        box_list = []
        for coord_id, coord in enumerate(pose_coords):
            if isinstance(coord, list):
                # instance = self.drawModel([coord[0], coord[1] + offset, coord[2]], coord_id, box)
                instance = self.drawModel([coord[0]*factor+offset, coord[1]*factor+offset, coord[2]*factor], coord_id, box)
            else:
                # instance = self.drawModel([coord.x, coord.y + offset, coord.z], coord_id, box)
                instance = self.drawModel([coord.x*factor+offset, coord.y*factor+offset, coord.z*factor], coord_id, box)
            box_list.append(instance)

        if with_line:
            line_list = []
            line_list.append(self.draw_line(pose_coords[0], pose_coords[1], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[0], pose_coords[4], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[3], pose_coords[1], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[3], pose_coords[7], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[4], pose_coords[6], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[8], pose_coords[6], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[9], pose_coords[10], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[11], pose_coords[12], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[11], pose_coords[13], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[12], pose_coords[14], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[11], pose_coords[23], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[12], pose_coords[24], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[23], pose_coords[24], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[14], pose_coords[16], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[16], pose_coords[18], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[16], pose_coords[22], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[16], pose_coords[20], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[18], pose_coords[20], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[13], pose_coords[15], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[15], pose_coords[21], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[15], pose_coords[19], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[15], pose_coords[17], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[19], pose_coords[17], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[24], pose_coords[26], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[23], pose_coords[25], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[27], pose_coords[25], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[28], pose_coords[26], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[28], pose_coords[30], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[28], pose_coords[32], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[30], pose_coords[32], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[27], pose_coords[29], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[27], pose_coords[31], factor, offset, offset))
            line_list.append(self.draw_line(pose_coords[29], pose_coords[31], factor, offset, offset))

    def drawModel(self, coord, name, model):
        """
        绘制模型
        :param coord: 要绘制的位置
        :param name: 模型名称
        :param model: 模型对象
        :return: 绘制的模型对象
        """
        instance = pc.NodePath(str(name))
        instance.reparentTo(self.render)
        if isinstance(coord, list):
            instance.setPos(coord[0], coord[1], coord[2])
        else:
            instance.setPos(coord.x, coord.y, coord.z)
        model.instanceTo(instance)
        return instance

    def draw_line(self, start, end, factor=1, offset_x=0, offset_y=0, offset_z=0):
        """
        绘制线段
        :param start: 线条起点
        :param end: 线条终点
        :param factor: 缩放因子，默认为1
        :param offset_x: x轴偏移，默认为0
        :param offset_y: y轴偏移，默认为0
        :param offset_z: z轴偏移，默认为0
        """
        # 创建LineSegs对象
        lines = pc.LineSegs()
        # 设置线条的颜色和宽度
        lines.setColor(1, 1, 1, 1)  # 白色
        lines.setThickness(2)  # 宽度为2
        # 添加线条的顶点
        if isinstance(start, list) and isinstance(end, list):
            lines.moveTo(start[0]*factor+offset_x, start[1]*factor+offset_y, start[2]*factor+offset_z)
            lines.drawTo(end[0]*factor+offset_x, end[1]*factor+offset_y, end[2]*factor+offset_z)
        else:
            lines.moveTo(start.x*factor+offset_x, start.y*factor+offset_y, start.z*factor+offset_z)
            lines.drawTo(end.x*factor+offset_x, end.y*factor+offset_y, end.z*factor+offset_z)
        # 创建线条的节点
        node = lines.create()
        # 创建线条的GeomNode，并添加到场景中
        line_node = self.render.attachNewNode(node)
        return line_node

    def rigRotation(self, name: str, rotation=None, dampener: float = 1, lerpTime: float = 0.3):
        """
        设置骨骼的位置
        :param name: 骨骼名称
        :param rotation: 要旋转的角度
        :param dampener: 阻尼器
        :param lerpTime: 插值所用时间
        """
        joint_name = self.skeleton_map[name]
        # 作为类成员保存骨骼
        if name not in self.skeleton.keys():
            self.skeleton[name] = self.actor.controlJoint(None, "modelRoot", joint_name)
        # 若获取不到骨骼，则不进行操作
        if self.skeleton[name] is None:
            return
        # 保存初始旋转角度
        if name not in self.init_rotation.keys():
            self.init_rotation[name] = Vector(
                self.skeleton[name].getH(),
                self.skeleton[name].getP(),
                self.skeleton[name].getR()
            )
        # 若未传入旋转角度，则使用初始旋转角度
        if rotation is None:
            rotation = Vector(self.skeleton[name].getH(), self.skeleton[name].getP(), self.skeleton[name].getR())

        # 使用阻尼器减缓变化
        x = rotation.x * dampener
        y = rotation.y * dampener
        z = rotation.z * dampener

        # 弧度制转角度制
        x = x * 180 / math.pi
        y = y * 180 / math.pi
        z = z * 180 / math.pi

        # 根据定义好的变换，设置旋转角度
        # bind_map = self.model_dict["binding"][name]["func"]
        # euler = pc.Vec3(
        #     self.init_rotation[name].x + eval(bind_map['fx']),
        #     self.init_rotation[name].y + eval(bind_map['fy']),
        #     self.init_rotation[name].z + eval(bind_map['fz'])
        # )
        euler = pc.Vec3(
            self.init_rotation[name].x + z,
            self.init_rotation[name].y - y,
            self.init_rotation[name].z + x
        )
        # self.skeleton[name].setHpr(euler)
        # 保存插值到Parallel中，等待一起执行
        interval = LerpHprInterval(self.skeleton[name], lerpTime, euler, self.skeleton[name].getHpr())
        # interval = self.skeleton[name].hprInterval(lerpTime, euler)
        self.parallel_interval.append(interval)

    def rigPosition(self, name, position=None, dampener: float = 1, lerpTime: float = 0.3):
        """
        设置骨骼的位置
        :param name: 骨骼名称
        :param position: 要移动到的位置
        :param dampener: 阻尼器
        :param lerpTime: 插值所用时长
        """
        joint_name = self.skeleton_map[name]
        # 作为类成员保存骨骼
        if name not in self.skeleton.keys():
            self.skeleton[name] = self.actor.controlJoint(None, "modelRoot", joint_name)
        # 若获取不到骨骼，则不进行操作
        if self.skeleton[name] is None:
            return
        # 保存初始位置
        if not(name in self.init_position.keys()):
            self.init_position[name] = Vector(
                self.skeleton[name].getX(),
                self.skeleton[name].getY(),
                self.skeleton[name].getZ()
            )
        # 若未传入位置，则使用初始位置
        if position is None:
            position = Vector(self.skeleton[name].getX(), self.skeleton[name].getY(), self.skeleton[name].getZ())

        # 使用阻尼器减缓变化
        x = position.x * dampener
        y = position.y * dampener
        z = position.z * dampener

        # 根据定义好的变换，设置位置
        bind_map = self.model_dict["binding"][name]["func"]
        vector = pc.Vec3(
            eval(bind_map['fx']),
            eval(bind_map['fy']),
            eval(bind_map['fz'])
        )
        # 保存插值到Parallel中，等待一起执行
        interval = self.skeleton[name].posInterval(lerpTime, vector)
        self.parallel_interval.append(interval)

    def setSkeleton(self, pose_coords_3d, pose_coords_2d, fps: int = 30):
        """
        设置骨骼
        """
        # 若正在播放动画，则丢弃当前传入帧数据
        if self.parallel_interval.isPlaying():
            return

        # self.draw_reference_coord(pose_coords_3d, self.factor)

        # 通过3D坐标和2D坐标，计算出骨骼的旋转角度和位置
        riggedPose = PoseSolver.solve(pose_coords_3d, pose_coords_2d)

        # lerp_time = 1 / fps
        lerp_time = 0.3

        # 设置骨骼
        self.rigRotation("Hips", riggedPose["Hips"]["rotation"], 0.7, lerp_time)

        # position = Vector(
        #     riggedPose["Hips"]["position"].x + self.position_offset["x"],
        #     riggedPose["Hips"]["position"].y + self.position_offset["y"],  # 升高一点
        #     -riggedPose["Hips"]["position"].z + self.position_offset["z"]  # 反向
        # )
        # self.rigPosition("Hips", position, 1, lerp_time)

        self.rigRotation("Chest", riggedPose["Spine"], 0.25, lerp_time)
        self.rigRotation("Spine", riggedPose["Spine"], 0.45, lerp_time)
        body_dampener = 1
        arm_dampener = body_dampener
        self.rigRotation("RightUpperArm", riggedPose["RightUpperArm"], arm_dampener, lerp_time)
        self.rigRotation("RightLowerArm", riggedPose["RightLowerArm"], arm_dampener, lerp_time)
        self.rigRotation("LeftUpperArm", riggedPose["LeftUpperArm"], arm_dampener, lerp_time)
        self.rigRotation("LeftLowerArm", riggedPose["LeftLowerArm"], arm_dampener, lerp_time)
        leg_dampener = body_dampener
        self.rigRotation("LeftUpperLeg", riggedPose["LeftUpperLeg"], leg_dampener, lerp_time)
        self.rigRotation("LeftLowerLeg", riggedPose["LeftLowerLeg"], leg_dampener, lerp_time)
        self.rigRotation("RightUpperLeg", riggedPose["RightUpperLeg"], leg_dampener, lerp_time)
        self.rigRotation("RightLowerLeg", riggedPose["RightLowerLeg"], leg_dampener, lerp_time)

        # 执行插值
        self.parallel_interval.start()

    def runTest(self):
        self.cam.setPos(0, -28, 6)
        self.testModel = self.loader.loadModel('panda')
        self.testModel.reparentTo(self.render)
        self.testModel.getPos()
        self.rotateInterval = LerpHprInterval(self.testModel, 3, Point3(360, 0, 0))
        self.rotateInterval.loop()


if __name__ == "__main__":
    # lol teh hobo
    panHandler = PandaHandler()

    app = QApplication(sys.argv)
    pandaWidget = QtPandaWidget()
    pandaWidget.setShowArea()
    pandaWidget.setTexture(panHandler.screenTexture)
    panHandler.runTest()
    pandaWidget.show()

    sys.exit(app.exec())
