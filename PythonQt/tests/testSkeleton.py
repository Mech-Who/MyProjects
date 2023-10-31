import panda3d.core as pc
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
import direct.interval.LerpInterval as lerp

import os
import math
import json
import numpy as np
import cv2
import mediapipe as mp


class App(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.model = None
        self.jointMap = None
        self.skeletonMap = None
        with open("./models.json", "r", encoding="utf-8") as model_json:
            self.json_info = json.load(model_json)
        self.setModel()
        self.skeletonMapping()

    def setModel(self):
        #self.model = Actor(self.loader.load_model("models/panda"))
        model_info = self.json_info["fddn"]
        model_file = os.path.abspath(model_info["model_root"] + model_info["asset_name"])
        self.model = Actor(self.loader.loadModel(pc.Filename.from_os_specific(model_file)))
        default_position = model_info["default_position"]
        default_hpr = model_info["default_hpr"]
        default_scale = model_info["default_scale"]
        self.model.setPos(default_position["x"], default_position["y"], default_position["z"])
        self.model.setHpr(default_hpr["x"], default_hpr["y"], default_hpr["z"])
        self.model.setScale(default_scale["x"], default_scale["y"], default_scale["z"])
        self.model.reparentTo(self.render)

    def skeletonMapping(self):
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

    def setFrame(self, pose_coords):
        """根据坐标，控制骨骼"""
        for key, value in self.skeletonMap.items():
            # 获得骨骼节点
            joint_node = self.model.controlJoint(None, "modelRoot", self.jointMap[key])
            # 获得骨骼节点的位置
            start = pc.Vec3(pose_coords[value[0]][0], pose_coords[value[0]][1], pose_coords[value[0]][2])
            end = pc.Vec3(pose_coords[value[1]][0], pose_coords[value[1]][1], pose_coords[value[1]][2])
            # 获取joint节点的起点和终点位置

            joint_start = joint_node.getParent().getPos()
            joint_end = joint_node.getPos()

            # 获得骨骼节点的四元数
            bone_vector = (end - start).normalized()
            ref_vector = pc.Vec3(0, 1, 0)
            rotation_axis = (ref_vector.cross(bone_vector)).normalized()
            rotation_angle = math.acos(ref_vector.dot(bone_vector))
            w = math.cos(rotation_angle / 2)
            x = rotation_axis.x * math.sin(rotation_angle / 2)
            y = rotation_axis.y * math.sin(rotation_angle / 2)
            z = rotation_axis.z * math.sin(rotation_angle / 2)
            quat = pc.Quat(x, y, z, w)
            # 获得骨骼节点的缩放
            pose_length = (end - start).length()
            # 计算joint节点的长度
            model_length = (joint_end - joint_start).length()

            # 获取骨骼节点的父节点和自身的变换矩阵
            self_mat = joint_node.getNetTransform().getMat()
            parent_mat = joint_node.getParent().getNetTransform().getMat()
            # 将骨骼节点的父节点的变换矩阵取逆，得到父节点到世界坐标系的变换矩阵
            parent_to_world_mat = parent_mat.invert()
            # 计算骨骼节点在世界坐标系下的坐标
            joint_pos = self_mat.xformPoint(pc.LPoint3(0, 0, 0)) * parent_to_world_mat
            # 计算骨骼节点在世界坐标系下的位置和父节点在世界坐标系下的位置之间的距离
            model_length = (joint_pos - parent_mat.xformPoint(pc.LPoint3(0, 0, 0))).length()

            scale = pose_length / model_length
            # 动画插值设置骨骼位置
            lerp.LerpPosQuatScaleInterval(joint_node, 3, start, quat, (scale, scale, scale)).start()
        pass


#  配置mediapipe的holistic算法
mp_holistic = mp.solutions.holistic
drawing = mp.solutions.drawing_utils

with mp_holistic.Holistic(static_image_mode=False,
                          model_complexity=1,
                          smooth_landmarks=True,
                          min_detection_confidence=0.5,
                          min_tracking_confidence=0.5
                          ) as holistic:
    # 1. 读取图片
    # capture = cv2.VideoCapture(0)
    # while capture.isOpened():
    #     ret, image = capture.read()
    #     image = cv2.flip(image, 1)
    file_name = "C:/Users/HP/Pictures/Camera Roll/test2.jpg"
    image = cv2.imread(file_name)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 2. Mediapipe处理
    results = holistic.process(image)

    # 3.原图绘制关键点,绘制人体关键点
    drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_holistic.POSE_CONNECTIONS)

    # 3.2 根据BlazePose谷歌模型的关键点划分,划分数据,坐标系变换
    pose_world_coords = np.array([[lmk.x, lmk.z, -lmk.y] for lmk in results.pose_world_landmarks.landmark])

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # cv2.imshow("image", image)

    # 3.3 查找骨骼映射
    app = App()
    app.setFrame(pose_world_coords)
    app.run()

    key = cv2.waitKey(0)
    if key & 0xFF == 'q':
        exit(0)
