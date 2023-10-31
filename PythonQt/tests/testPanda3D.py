import json
import os
import pprint
import math

from direct.filter.CommonFilters import CommonFilters
from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Parallel
import panda3d.core as p3d

from kalidokit4python.Util.Vector import Vector
from kalidokit4python.Pose.PoseSolver import PoseSolver
from MyKalidoKit.CalcArm import calcArm, calcHand
from MyKalidoKit.CalcLeg import calcLeg

p3d.loadPrcFile("./config.prc")


class MyApp(ShowBase):
    # 定义成员变量
    model = None
    actor = None
    model_dict = None
    directLightNode = None
    ambientLightNode = None
    velocity = None
    skeleton_map = None
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
    riggedPose = None
    keyMap = None
    standard_position = None
    standard_rotation = None
    standard_scale = None
    init_rotation = {}

    status = None

    paralel_interval = Parallel()

    def __init__(self):
        ShowBase.__init__(self)

        # 设置模型
        self.setModels()
        # 设置灯光
        # self.setLight()
        # 设置事件
        # self.setEvents()

    def setModels(self):
        """
        设置模型
        """
        # 获得模型路径
        with open("./models.json", "r", encoding="utf-8") as f:
            json_content = json.load(f)
            self.model_dict = json_content["system_models"][-1]

        model_file = p3d.Filename.from_os_specific(os.path.abspath(self.model_dict["path"]))
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
        self.actor.setHpr(0, 0, 0)
        self.actor.setPos(0, 0, 20)

        self.standard_position = self.actor.getPos()
        self.standard_rotation = self.actor.getHpr()
        self.standard_scale = scale

        # 调整摄像机位置和朝向
        cam_distance = 2 * radius
        self.cam.setPos(0, -cam_distance, 0)
        self.cam.lookAt(0, 0, 0)

        # 根据设置二次微调模型
        # 根据cameraPosition、cameraRotation、cameraTarget调整摄像头中模型的位置、旋转和缩放
        position = self.model_dict["cameraPosition"]
        rotation = self.model_dict["cameraRotation"]
        scale = self.model_dict["cameraTarget"]

        # position
        self.actor.setPos(self.standard_position + p3d.Point3(*position.values()))
        # rotation
        self.actor.setHpr(self.standard_rotation + p3d.Point3(*rotation.values()))
        # scale
        self.actor.setScale(self.standard_scale * min(*scale.values()))

        # 绑定骨骼（手动版）
        # 设置骨骼映射表
        self.skeleton_map = {k: v["name"] for k, v in self.model_dict["binding"].items()}

        coord_sys_np = self.loader.loadModel("models/zup-axis")
        for name, bone in self.skeleton_map.items():
            bone_node = self.actor.exposeJoint(None, "modelRoot", bone)
            coord_sys = p3d.NodePath(f"coord_{name}")
            coord_sys.reparentTo(bone_node)
            instance = coord_sys_np.instanceTo(coord_sys)
            instance.setPos(0, 0, 0)
            instance.setHpr(0, 0, 0)
            instance.setScale(1)
            # self.actor.releaseJoint("modelRoot", bone)

    def setLight(self):
        """
        设置灯光
        """
        # panda3d的内置对象base，设置背景颜色为纯白
        # self.setBackgroundColor(1, 1, 1, 1)

        # 设置光辉
        filters = CommonFilters(self.win, self.cam)
        filters.setBloom(size="small")

        # 设置灯光
        # 定向光
        direct_light = p3d.DirectionalLight('direction light')
        direct_light.setColor((1, 1, 1, 1))  # red green blue alpha
        self.directLightNode = self.render.attachNewNode(direct_light)
        # 环境光
        ambient_light = p3d.AmbientLight('ambient light')
        ambient_light.setColor((0.2, 0.2, 0.2, 1))
        self.ambientLightNode = self.render.attachNewNode(ambient_light)

    def setEvents(self):
        """
        绑定按键事件
        """
        # 设置速度
        self.velocity = {
            "walk": 4,
            "run": 10,
            "rotate": 5
        }

        # 设置按键状态的map
        self.keyMap = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False,
            "rotateForward": False,
            "rotateBackward": False,
            "rotateLeft": False,
            "rotateRight": False,
            "rotateUp": False,
            "rotateDown": False,
        }

        # 前进
        self.accept("w", self.updateKeyMap, ["forward", True])
        self.accept("w-up", self.updateKeyMap, ["forward", False])
        # 左移
        self.accept("a", self.updateKeyMap, ["left", True])
        self.accept("a-up", self.updateKeyMap, ["left", False])
        # 后退
        self.accept("s", self.updateKeyMap, ["backward", True])
        self.accept("s-up", self.updateKeyMap, ["backward", False])
        # 右移
        self.accept("d", self.updateKeyMap, ["right", True])
        self.accept("d-up", self.updateKeyMap, ["right", False])
        # 上升
        self.accept("space", self.updateKeyMap, ["up", True])
        self.accept("space-up", self.updateKeyMap, ["up", False])
        # 下降
        self.accept("control", self.updateKeyMap, ["down", True])
        self.accept("control-up", self.updateKeyMap, ["down", False])
        # 前旋转
        self.accept("z", self.updateKeyMap, ["rotateForward", True])
        self.accept("z-up", self.updateKeyMap, ["rotateForward", False])
        # 后旋转
        self.accept("c", self.updateKeyMap, ["rotateBackward", True])
        self.accept("c-up", self.updateKeyMap, ["rotateBackward", False])
        # 左旋转
        self.accept("q", self.updateKeyMap, ["rotateLeft", True])
        self.accept("q-up", self.updateKeyMap, ["rotateLeft", False])
        # 右旋转
        self.accept("e", self.updateKeyMap, ["rotateRight", True])
        self.accept("e-up", self.updateKeyMap, ["rotateRight", False])
        # 上旋转
        self.accept("r", self.updateKeyMap, ["rotateUp", True])
        self.accept("r-up", self.updateKeyMap, ["rotateUp", False])
        # 下旋转
        self.accept("f", self.updateKeyMap, ["rotateDown", True])
        self.accept("f-up", self.updateKeyMap, ["rotateDown", False])

        # 设置task管理器
        self.taskMgr.add(self.move, "update")

    def updateKeyMap(self, key, state):
        """
        更新按键状态
        :param key: 按键名称
        :param state: 按键状态
        """
        self.keyMap[key] = state

    def move(self, task):
        """
        根据按键状态设置模型位置
        :param task: 传入task对象
        :return: task结束状态，cont代表转移至其他状态，done代表结束
        """
        dt = globalClock.getDt()
        pos = self.actor.getPos()
        if self.keyMap["forward"]:
            pos.y += self.velocity["walk"] * dt
        if self.keyMap["backward"]:
            pos.y -= self.velocity["walk"] * dt
        if self.keyMap["left"]:
            pos.x -= self.velocity["walk"] * dt
        if self.keyMap["right"]:
            pos.x += self.velocity["walk"] * dt
        if self.keyMap["up"]:
            pos.z += self.velocity["walk"] * dt
        if self.keyMap["down"]:
            pos.z -= self.velocity["walk"] * dt
        if self.keyMap["rotateForward"]:
            self.actor.setR(self.actor.getR() + self.velocity["rotate"] * dt * 30)
        if self.keyMap["rotateBackward"]:
            self.actor.setR(self.actor.getR() - self.velocity["rotate"] * dt * 30)
        if self.keyMap["rotateLeft"]:
            self.actor.setH(self.actor.getH() + self.velocity["rotate"] * dt * 30)
        if self.keyMap["rotateRight"]:
            self.actor.setH(self.actor.getH() - self.velocity["rotate"] * dt * 30)
        if self.keyMap["rotateUp"]:
            self.actor.setP(self.actor.getP() + self.velocity["rotate"] * dt * 30)
        if self.keyMap["rotateDown"]:
            self.actor.setP(self.actor.getP() - self.velocity["rotate"] * dt * 30)
        self.actor.setPos(pos)
        return task.cont

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

    def draw_line(self, start, end, factor=1, offset_x=0, offset_y=0, offset_z=0):
        # 创建LineSegs对象
        lines = p3d.LineSegs()
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

    def draw_origin(self):
        """
        绘制坐标原点位置
        """
        # 设置原点
        origin = self.loader.loadModel("models/zup-axis")
        origin.setScale(0.5)
        self.drawModel([-20, -20, 0], "Origin", origin)

    def drawModel(self, coord, name, model):
        """
        绘制模型
        :param coord: 要绘制的位置
        :param name: 模型名称
        :param model: 模型对象
        :return: 绘制的模型对象
        """
        instance = p3d.NodePath(str(name))
        instance.reparentTo(self.render)
        if isinstance(coord, list):
            instance.setPos(coord[0], coord[1], coord[2])
        else:
            instance.setPos(coord.x, coord.y, coord.z)
        model.instanceTo(instance)
        return instance

    def setFrame(self, pose_coords_3d, pose_coords_2d):
        """
        设置一帧的动作
        """
        # 如果未准备好则抛弃该帧图像数据，直接return
        if self.paralel_interval.isPlaying():
            return
        # pose_coords = utils.calculate_coords(pose_coords)
        self.draw_origin()
        # 设置坐标偏移量
        offset = -20
        factor = 20
        self.draw_reference_coord(pose_coords_3d, factor, offset)

        # # 手臂调整
        # # 左臂
        # leftUpperArm = self.actor.controlJoint(None, "modelRoot", self.skeleton_map["LeftUpperArm"])
        # calcArm(leftUpperArm, pose_coords_3d, 13, 11, 12)
        # leftLowerArm = self.actor.controlJoint(None, "modelRoot", self.skeleton_map["LeftLowerArm"])
        # calcArm(leftLowerArm, pose_coords_3d, 15, 13, 11)
        # leftHand = self.actor.controlJoint(None, "modelRoot", self.skeleton_map["LeftHand"])
        # calcHand(leftHand, pose_coords_3d, 19, 17, 15, 13)
        # # 右臂
        # rightUpperArm = self.actor.controlJoint(None, "modelRoot", self.skeleton_map["RightUpperArm"])
        # calcArm(rightUpperArm, pose_coords_3d, 14, 12, 11)
        # rightLowerArm = self.actor.controlJoint(None, "modelRoot", self.skeleton_map["RightLowerArm"])
        # calcArm(rightLowerArm, pose_coords_3d, 16, 14, 12)
        # rightHand = self.actor.controlJoint(None, "modelRoot", self.skeleton_map["RightHand"])
        # calcHand(rightHand, pose_coords_3d, 20, 18, 16, 14)
        #
        # # 腿部调整
        # # 左腿
        # leftUpperLeg = self.actor.controlJoint(None, "modelRoot", self.skeleton_map["LeftUpperLeg"])
        # calcLeg(leftUpperLeg, pose_coords_3d, 25, 23, 24)
        # leftLowerLeg = self.actor.controlJoint(None, "modelRoot", self.skeleton_map["LeftLowerLeg"])
        # calcLeg(leftLowerLeg, pose_coords_3d, 27, 25, 23)
        # # 右腿
        # rightUpperLeg = self.actor.controlJoint(None, "modelRoot", self.skeleton_map["RightUpperLeg"])
        # calcLeg(rightUpperLeg, pose_coords_3d, 26, 24, 23)
        # rightLowerLeg = self.actor.controlJoint(None, "modelRoot", self.skeleton_map["RightLowerLeg"])
        # calcLeg(rightLowerLeg, pose_coords_3d, 28, 26, 24)

        # # 左手旋转90°测试
        # leftLowerArm = self.actor.controlJoint(None, "modelRoot", self.skeleton_map["LeftLowerArm"])
        # quat = p3d.QuatF()
        # quat.setHpr(p3d.Vec3F(0, 90, 0))
        # leftLowerArm.setQuat(quat)

        self.riggedPose = PoseSolver.solve(pose_coords_3d, pose_coords_2d)
        # pprint.pprint(self.riggedPose)

        # Hips
        self.rigRotation("Hips", self.riggedPose["Hips"]["rotation"], 0.05)
        position = Vector(
                # self.riggedPose["Hips"]["position"].x + 0,  # Reverse direction
                0,
                # self.riggedPose["Hips"]["position"].y + 1,  # Add a bit of height
                0,
                # -self.riggedPose["Hips"]["position"].z + 0  # Reverse direction
                0
        )
        self.rigPosition("Hips", position, 1, 0.01)
        self.rigRotation("Chest", self.riggedPose["Spine"], 0.03)
        self.rigRotation("Spine", self.riggedPose["Spine"], 0.05)
        # Arms
        arm_dampener = 1
        # RightArm
        self.rigRotation("RightUpperArm", self.riggedPose["RightUpperArm"], arm_dampener)  # rig会有影响
        self.rigRotation("RightLowerArm", self.riggedPose["RightLowerArm"], arm_dampener)
        self.rigRotation("RightHand", self.riggedPose["RightHand"], arm_dampener)
        # LeftArm
        self.rigRotation("LeftUpperArm", self.riggedPose["LeftUpperArm"], arm_dampener)  # rig会有影响
        self.rigRotation("LeftLowerArm", self.riggedPose["LeftLowerArm"], arm_dampener)
        self.rigRotation("LeftHand", self.riggedPose["LeftHand"], arm_dampener)
        # Legs
        leg_dampener = 0.2
        # RightLeg
        self.rigRotation("RightUpperLeg", self.riggedPose["RightUpperLeg"], leg_dampener)
        self.rigRotation("RightLowerLeg", self.riggedPose["RightLowerLeg"], leg_dampener)
        # LeftLeg
        self.rigRotation("LeftUpperLeg", self.riggedPose["LeftUpperLeg"], leg_dampener)
        self.rigRotation("LeftLowerLeg", self.riggedPose["LeftLowerLeg"], leg_dampener)

        self.paralel_interval.start()

    def rigRotation(self, name: str, rotation=None, dampener: float = 1, lerpTime: float = 0.3):
        joint_name = self.skeleton_map[name]
        Part = self.actor.controlJoint(None, "modelRoot", joint_name)
        if Part is None:
            return
        if not(name in self.init_rotation.keys()):
            self.init_rotation[name] = Vector(Part.getH(), Part.getP(), Part.getR())
        if rotation is None:
            rotation = Vector(Part.getH(), Part.getP(), Part.getR())

        x = rotation.x * dampener * 180 / math.pi
        y = rotation.y * dampener * 180 / math.pi
        z = rotation.z * dampener * 180 / math.pi

        euler = p3d.Vec3(
            self.init_rotation[name].x + x,
            self.init_rotation[name].y + y,
            self.init_rotation[name].z + z
        )

        rotation = p3d.QuatF()
        rotation.setHpr(euler)
        interval = Part.hprInterval(lerpTime, euler)
        self.paralel_interval.append(interval)

        # quat = p3d.QuatF()
        # quat.setHpr(euler)
        # Part.setQuat(quat)
        # Part.quaternion.slerp(quaternion, lerpAmount)  # interpolate
        # self.actor.releaseJoint("modelRoot", joint_name)

    def lerpOver(self):
        print(f"current state: {self.status}")
        self.status = "ready"
        print(f"current state: {self.status}")

    def rigPosition(self, name, position=None, dampener: float = 1, lerpTime: float = 0.3):
        """
        设置骨骼的位置
        :param name: 骨骼名称
        :param position: 要移动到的位置
        :param dampener: 阻尼器
        :param lerpAmount: 每隔lerpAmount值进行一次插值
        """
        joint_name = self.skeleton_map[name]
        Part = self.actor.controlJoint(None, "modelRoot", joint_name)
        if position is None:
            position = Vector(Part.getX(), Part.getY(), Part.getZ())
        if Part is None:
            return
        x = position.x * dampener
        y = position.y * dampener
        z = position.z * dampener
        # bind_map = self.model_dict["binding"][name]["func"]
        # vector = p3d.Vec3(
        #     eval(bind_map['fx']),
        #     eval(bind_map['fy']),
        #     eval(bind_map['fz'])
        # )
        vector = p3d.Vec3(x, z, -y)
        Part.setPos(vector)
        # interval = Part.posInterval(lerpTime, vector)
        # self.paralel_interval.append(interval)


if __name__ == "__main__":
    app = MyApp()
    app.run()
