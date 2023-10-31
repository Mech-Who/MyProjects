import json
import math
import os

import numpy as np
from direct.filter.CommonFilters import CommonFilters
from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from direct.actor.Actor import Actor
import panda3d.core as p3d

# p3d.loadPrcFileData("", "window-type offscreen")


class PandaWindow(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # p3d.loadPrcFileData("", "window-type offscreen")

        # 定义成员变量
        self.anims = None
        self.model = None
        self.model_root = None
        self.json_info = None
        self.directLightNode = None
        self.ambientLightNode = None
        self.velocity = None
        self.jointMap = None
        self.keyMap = None
        self.skeletonMap = None

        # 设置模型
        self.setModels()
        # 设置灯光
        self.setLight()
        # 设置事件
        self.setEvents()

        self.screenTexture = p3d.Texture()
        self.screenTexture.setMinfilter(p3d.Texture.FTLinear)
        self.win.addRenderTexture(self.screenTexture, p3d.GraphicsOutput.RTMCopyRam)

    def setModels(self):
        """
        设置模型
        """
        # 获得模型路径
        with open("./models.json", "r", encoding="utf-8") as f:
            json_content = json.load(f)
            self.json_info = json_content["system_models"][-1]
        model_path = self.json_info["path"]

        # 加载模型到引擎
        model_file = p3d.Filename.from_os_specific(os.path.abspath(model_path))
        model_root = self.loader.loadModel(model_file)
        self.model = Actor(model_root)

        # 设置位置和缩放
        camera_position = self.json_info["cameraPosition"]
        camera_rotation = self.json_info["cameraRotation"]
        camera_scale = self.json_info["cameraTarget"]
        self.model.setPos(camera_position["x"], camera_position["y"], camera_position["z"])
        self.model.setHpr(camera_rotation["x"], camera_rotation["y"], camera_rotation["z"])
        self.model.setScale(camera_scale["x"], camera_scale["y"], camera_scale["z"])

        # 将模型添加到场景图
        self.model.reparentTo(self.render)

        # 绑定骨骼（手动版）
        self.buildSkeletonMap()

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
        pos = self.model.getPos()
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
            self.model.setR(self.model.getR() + self.velocity["rotate"] * dt * 30)
        if self.keyMap["rotateBackward"]:
            self.model.setR(self.model.getR() - self.velocity["rotate"] * dt * 30)
        if self.keyMap["rotateLeft"]:
            self.model.setH(self.model.getH() + self.velocity["rotate"] * dt * 30)
        if self.keyMap["rotateRight"]:
            self.model.setH(self.model.getH() - self.velocity["rotate"] * dt * 30)
        if self.keyMap["rotateUp"]:
            self.model.setP(self.model.getP() + self.velocity["rotate"] * dt * 30)
        if self.keyMap["rotateDown"]:
            self.model.setP(self.model.getP() - self.velocity["rotate"] * dt * 30)
        self.model.setPos(pos)
        return task.cont

    def setFirstFrame(self, pose_coords):
        """
        设置第一帧动作
        """
        joint_node = self.model.controlJoint(None, "modelRoot", self.jointMap["Head"])

    def drawModel(self, coord, name, model):
        """
        在提供的坐标点上，绘制模型
        :param coord: 要绘制的位置
        :param name: 模型名称
        :param model: 模型对象
        :return: 绘制的模型对象
        """
        instance = p3d.NodePath(str(name))
        instance.reparentTo(self.render)
        instance.setPos(coord[0], coord[1], coord[2])
        model.instanceTo(instance)
        return instance

    def draw_reference_coord(self, offset, pose_coords):
        """
        绘制基于关键点的参考模型
        """
        # 绘制关键点位置
        box = self.loader.loadModel("models/box")
        box.setScale(0.1)
        box_list = []
        for coord_id, coord in enumerate(pose_coords):
            instance = self.drawModel([coord[0], coord[1] + offset, coord[2]], coord_id, box)
            box_list.append(instance)

    def draw_origin(self):
        """
        在世界坐标系的原点位置绘制一个坐标系
        """
        # 设置原点
        origin = self.loader.loadModel("models/zup-axis")
        origin.setScale(0.1)
        self.drawModel([0, 0, 0], "Origin", origin)

    def setFrame(self, pose_coords):
        """
        设置一帧的动作，
        """
        # 添加通过计算得到的额外坐标点ABCDE
        pose_coords = self.calculate_coords(pose_coords)
        # 在原点位置绘制世界坐标系
        self.draw_origin()
        # 设置坐标偏移量，并在关键点绘制参考模型
        offset = 10
        self.draw_reference_coord(offset, pose_coords)
        # 设置每一个骨骼
        skeleton_list = ["Neck", "Chest", "Spine", "Hips", "LeftUpperLeg", "LeftLowerLeg", "RightUpperLeg",
                         "RightLowerLeg", "LeftFoot", "RightFoot", "LeftUpperArm", "LeftLowerArm", "RightUpperArm",
                         "RightLowerArm", "LeftHand", "RightHand"]
        for skel in skeleton_list:
            self.set_skel(pose_coords, skel, offset)

    def set_skel(self, pose_coords, skel, offset=0):
        """
        设置一个骨骼的姿态，逻辑如下：
        1. 根据Holistic算法输出的pose_world_landmark中的关键点坐标，获取对应的骨骼起点和终点的坐标，并存储在一个字典中。
        2. 根据字典中存储的坐标数据，依次获取每个骨骼对应的Joint节点。
        3. 将每个Joint节点的位置设置为对应的骨骼起点坐标，并将其旋转到与骨骼方向一致的方向。
        4. 可以使用Panda3D提供的方法来进行旋转操作，例如setHpr()方法。其中，Hpr是指Yaw、Pitch、Roll三个角度值。
           可以根据两个骨骼起点和终点的坐标计算出一个向量，再根据该向量生成Hpr值，将Joint节点旋转到对应的方向。
        5. 依次处理所有的骨骼，完成模型的姿态设置。
        :param pose_coords: mediapipe获得的坐标数组
        :param skel: 要设置的骨骼
        :param offset: y轴偏移量，默认为0
        """
        joint_node, start, end = self.get_joint_by_skel(pose_coords, skel, offset)
        # 绘制参考关键点
        for_model = self.loader.loadModel("models/smiley")
        for_model.setScale(0.05)
        self.drawModel([start[0], start[1] - 3, start[2]], skel, for_model)
        ######################################### 计算Joint姿态 ##########################################
        # 1. 计算hpr
        # 以Y轴为上方向，计算从起点到终点的方向向量
        direction = end - start
        direction.normalize()
        # 计算hpr值，使模型面向方向向量
        # 计算弧度制旋转角度
        h = math.atan2(direction.getY(), direction.getX()) * 180 / math.pi
        p = math.asin(direction.getZ()) * 180 / math.pi
        r = 0.0  # 由于方向向量不包含bank轴的旋转，因此此处为0
        hpr = p3d.LVector3f(h, p, r)
        ######################################### 设置Joint姿态 ##########################################
        # 根据start坐标设置位置，根据hpr设置旋转
        # 插值动画函数：
        # lerp.LerpPosInterval(joint_node, 1, start)
        # lerp.LerpHprInterval(joint_node, 1, hpr)
        # lerp.LerpScaleInterval(joint_node, 1, 1)
        # lerp.LerpQuatInterval(joint_node, 1, p3d.Quat(hpr))
        print("##############################################")
        origin_transform = joint_node.getTransform()
        print(f"origin_transform: {origin_transform}")
        print(f"start: {start}, hpr:{hpr}")
        scale_times = 0.01
        scale = p3d.LVecBase3(scale_times, scale_times, scale_times)
        shear = origin_transform.getShear()
        new_transform = p3d.TransformState.makePosHprScaleShear(start, hpr, scale, shear)
        print(f"new_transform: {new_transform}")
        joint_node.setTransform(self.render, new_transform)

    def get_joint_by_skel(self, pose_coords, skel, offset=0):
        """
        根据骨骼名称获取对应的Joint节点，并返回Joint的起点和终点坐标，需要提供图像中的关键点坐标
        offset为Y轴偏移量，可有可无，主要是防止想要绘制多个模型时，多个模型重合
        :returns: joint_node, start, end
        """
        # 获取joint名和对应的关键点
        joint_name = self.jointMap[skel]
        key = self.skeletonMap[skel]
        # 获得Joint节点
        joint_node = self.model.controlJoint(None, "modelRoot", joint_name)
        # 获得骨骼起点和终点的坐标
        start = p3d.Vec3(pose_coords[key[0]][0], pose_coords[key[0]][1] + offset, pose_coords[key[0]][2])
        end = p3d.Vec3(pose_coords[key[1]][0], pose_coords[key[1]][1] + offset, pose_coords[key[1]][2])
        return joint_node, start, end

    def calculate_coords(self, pose_coords):
        """
        基于Mediapipe骨骼模型，再计算额外的关键点坐标，主要是人体脊椎的几个点。
        额外点分别基座ABCDE点，从上往下依次排列，C是AE中点，B和D分别是AC和CE的中点
        """
        # 计算额外点
        coord_A = (pose_coords[9] + pose_coords[10]) / 2
        coord_B = (pose_coords[12] + pose_coords[11]) / 2
        coord_E = (pose_coords[23] + pose_coords[24]) / 2
        coord_mid = (coord_B + coord_E) / 2
        coord_C = (coord_B + coord_mid) / 2
        coord_D = (coord_mid + coord_E) / 2
        # 计算缩放因子，例：mediapipe关键点腿长为0.5，而模型腿长为0.8，所以缩放因子为0.8/0.5=1.6
        mediapipe_leg = np.linalg.norm(
            pose_coords[self.skeletonMap["LeftUpperLeg"][0]] - pose_coords[self.skeletonMap["LeftUpperLeg"][1]])
        leg_joint = self.model.exposeJoint(None, "modelRoot", self.jointMap["LeftUpperLeg"])
        model_leg = leg_joint.getTransform().getScale().length()
        scale_factor = model_leg / mediapipe_leg
        print(f"mediapipe_leg length:{mediapipe_leg}, leg joint length:{model_leg}, scale factor:{scale_factor}")
        # 添加额外点到pose_coords中，A-E分别对应33-37
        pose_coords = np.append(pose_coords, [coord_A, coord_B, coord_C, coord_D, coord_E], axis=0) * 1
        return pose_coords

    def buildSkeletonMap(self):
        print("show skeleton:")
        print(f"type: {type(self.model)}, info: {self.model.getActorInfo()}")
        self.skeletonMap = {
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
        # 默认设置
        # 本应由用户设置
        self.jointMap = {
            "Neck": "Neck_Fredina_Armature_7_12",
            "Chest": "Spine_1_Fredina_Armature_6_11",
            "Spine": "Spine_Fredina_Armature_5_10",
            "Hips": "Root_Fredina_Armature_4_9",
            "LeftUpperLeg": "Thigh.L_Fredina_Armature_92_97",
            "LeftLowerLeg": "Calf.L_Fredina_Armature_93_98",
            "RightUpperLeg": "Thigh.R_Fredina_Armature_84_89",
            "RightLowerLeg": "Calf.R_Fredina_Armature_85_90",
            "LeftFoot": "Foot.L_Fredina_Armature_94_99",
            "RightFoot": "Foot.R_Fredina_Armature_86_91",
            "LeftUpperArm": "Upperarm.L_Fredina_Armature_63_68",
            "LeftLowerArm": "Forearm.L_Fredina_Armature_64_69",
            "RightUpperArm": "Upperarm.R_Fredina_Armature_41_46",
            "RightLowerArm": "Forearm.R_Fredina_Armature_42_47",
            "LeftHand": "Hand.L_Fredina_Armature_65_70",
            "RightHand": "Hand.R_Fredina_Armature_43_48"
        }
        # 获取骨骼名称
        joint_names = self.model.getJoints()
        with open("results/joint.txt", "w", encoding="utf-8") as f:
            for joint in joint_names:
                # print(f"joint: {joint}")
                f.write(f"{joint}\n")
        part_names = self.model.getPartNames()
        with open("results/part.txt", "w", encoding="utf-8") as f:
            for part in part_names:
                print(f"part: {part}")
                f.write(f"{part}\n")
        # self.model.controlJoint(None, "modelRoot", "modelRoot")