import os
import math
import json

import panda3d.core as p3d
from direct.actor.Actor import Actor
from direct.interval.MetaInterval import Sequence
from panda3d.core import LineSegs
from direct.showbase.ShowBase import ShowBase
import direct.extensions_native.Mat3_extensions
from scipy.spatial.transform import Rotation

import kalidokit4python.Util.Vector as Vec
from kalidokit4python.Util.Vector import Vector


def calcQuatFromVector(vector: list | tuple | p3d.Vec3):
    if not isinstance(vector, p3d.Vec3):
        vector = p3d.Vec3(vector[0], vector[1], vector[2])
    normalized_vector = vector.normalized()
    # 创建四元数
    quat = p3d.QuatF()
    quat.setFromAxisAngle(1, normalized_vector)
    return quat


def getRotationFromVector(from_vec, to_vec):
    """
    get rotation hpr or quat from 'from_vec' to 'to_vec'
    :param from_vec: start direction
    :param to_vec: end direction
    :return: hpr and quat from 'from_vec' to 'to_vec'
    """
    if not isinstance(from_vec, p3d.Vec3):
        from_vec = p3d.Vec3(from_vec[0], from_vec[1], from_vec[2])
    if not isinstance(to_vec, p3d.Vec3):
        to_vec = p3d.Vec3(to_vec[0], to_vec[1], to_vec[2])
    # 计算旋转轴
    normalized_from_vec = from_vec.normalized()
    normalized_to_vec = to_vec.normalized()
    axis = normalized_from_vec.cross(normalized_to_vec)
    axis.normalize()
    # 计算旋转角度
    angle = normalized_from_vec.angleDeg(normalized_to_vec)
    # 创建Quat对象
    quat = p3d.Quat()
    quat.setFromAxisAngle(angle, axis)
    # 获取HPR值
    hpr = quat.getHpr()

    return hpr, quat


def globalToLocalVector(vector, global_to_local):
    if not isinstance(vector, p3d.Vec3):
        vector = p3d.Vec3(vector[0], vector[1], vector[2])
    local_vector = p3d.Vec3(vector)
    local_vector = global_to_local.xformVec(local_vector)
    return local_vector


def mat4MultiplyVec4(global_to_local, vec):
    v1 = vec[0] * global_to_local[0][0] + vec[1] * global_to_local[0][1] + vec[2] * global_to_local[0][2] + vec[3] * \
         global_to_local[0][3]
    v2 = vec[0] * global_to_local[1][0] + vec[1] * global_to_local[1][1] + vec[2] * global_to_local[1][2] + vec[3] * \
         global_to_local[1][3]
    v3 = vec[0] * global_to_local[2][0] + vec[1] * global_to_local[2][1] + vec[2] * global_to_local[2][2] + vec[3] * \
         global_to_local[2][3]
    v4 = vec[0] * global_to_local[3][0] + vec[1] * global_to_local[3][1] + vec[2] * global_to_local[3][2] + vec[3] * \
         global_to_local[3][3]
    return p3d.Vec4(v1, v2, v3, v4)


def makeVecFromHpr(h, p, r):
    # 已知的HPR角度
    hpr = p3d.Vec3(h, p, r)
    direction_transform = p3d.TransformState.makeHpr(hpr)
    rotation_matrix = direction_transform.getMat()

    # 构造单位向量
    unit_vector = p3d.Vec3(1.0, 0.0, 0.0)  # 示例中假设方向为 x 轴正方向
    rotated_vector = rotation_matrix.xform(unit_vector)
    return rotated_vector


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.cam.setPos(0, -50, 0)
        self.cam.lookAt(0, 0, 0)

        axis = self.loader.loadModel("models/zup-axis")
        axis_node = self.drawModel([0, 0, 0], "axis", axis)

        # 加载模型和骨骼动画（如果适用）
        model_file = p3d.Filename.from_os_specific(os.path.abspath("../models/fredina_nude.glb"))

        self.actor = Actor(self.loader.loadModel(model_file))
        self.actor.reparentTo(self.render)

        self.actor.setScale(0.1)
        self.actor.setHpr(0, 180, 0)

        # 获得骨骼映射字典
        with open("./models.json", "r", encoding="utf-8") as f:
            json_content = json.load(f)
            self.model_dict = json_content["system_models"][-1]
        self.skeleton_map = {k: v["name"] for k, v in self.model_dict["binding"].items()}

        # 给要控制的骨骼加上坐标系
        coord_sys_np = self.loader.loadModel("models/zup-axis")
        # for name, bone in self.skeleton_map.items():
        #     bone_node = self.actor.exposeJoint(None, "modelRoot", bone)
        #     coord_sys = p3d.NodePath(f"coord_{name}")
        #     coord_sys.reparentTo(bone_node)
        #     instance = coord_sys_np.instanceTo(coord_sys)
        #     instance.setPos(0, 0, 0)
        #     instance.setHpr(0, 0, 0)
        #     instance.setScale(1.5)

        # 获得要设置的骨骼
        joint = self.actor.controlJoint(None, 'modelRoot', 'Forearm.L_Fredina_Armature_64_69')
        current_global_transform = joint.getTransform()
        current_hpr = current_global_transform.getHpr()  # 骨骼当前的方向向量
        current_vector = makeVecFromHpr(current_hpr[0], current_hpr[1], current_hpr[2])
        # current_vector = p3d.Vec3(current_vector[0], current_vector[1], current_vector[2])
        current_mat = current_global_transform.getMat()
        current_mat_inverse = p3d.Mat4(current_mat)
        current_mat_inverse.invertInPlace()
        # print(current_mat)
        # print(current_mat_inverse)
        # print(current_mat*current_mat_inverse)

        target_vector = p3d.Vec3(1, 1, 1)  # 指定的全局坐标系中的向量方向
        rotation = Rotation.from_rotvec(target_vector)
        euler_angles = rotation.as_euler('xyz', degrees=True)
        print(f"euler_angles:{euler_angles}")

        rotation_hpr, rotation_quat = getRotationFromVector(current_vector, target_vector)

        joint.setHpr(euler_angles[0], euler_angles[1], euler_angles[2])
        white_line = self.drawLine([0, 0, 0], target_vector*5, self.render, color=(1, 1, 1, 1), thickness=20)
        red_line = self.drawLine([0, 0, 0], current_vector*10, self.render, color=(1, 0, 0, 1), thickness=20)

    def LocalVectorUsedInModel(self):
        """
        测试局部坐标系的向量是否可以用于模型的旋转
        """
        white_line = self.drawLine([0, 0, 0], [3, 6, 9], self.render)
        red_line = self.drawLine([0, 0, 0], [0, 0, 3], self.render, color=(1, 0, 0, 1))
        green_line = self.drawLine([0, 0, 0], [0, 0, 3], self.render, color=(0, 1, 0, 1))
        blue_line = self.drawLine([0, 0, 0], [0, 0, 3], self.render, color=(0, 0, 1, 1))

        # 获取模型的全局坐标系和局部坐标系之间的变换矩阵
        global_to_local = white_line.getNetTransform().getMat()

        vec = [1, 2, 3]

        local_vec = globalToLocalVector(vec, global_to_local)
        print(local_vec)
        pass

    def GetQuat(self):
        """
        测试，基于向量获得旋转角度，用Quat或者Hpr值表示
        """
        start_vec = [3, 3, 3]
        white_line = self.drawLine([0, 0, 0], [3, 6, 9], self.render)
        red_line = self.drawLine([0, 0, 0], start_vec, self.render, color=(1, 0, 0, 1))
        green_line = self.drawLine([0, 0, 0], start_vec, self.render, color=(0, 1, 0, 1))
        blue_line = self.drawLine([0, 0, 0], start_vec, self.render, color=(0, 0, 1, 1))
        yellow_line = self.drawLine([0, 0, 0], start_vec, self.render, color=(0, 1, 1, 1))

        vec = [1, 2, 3]
        # 测试成功，说明这个方法可行
        hpr, quat = getRotationFromVector(start_vec, vec)
        print(f"hpr:{hpr}, quat:{quat}")
        red_line.setQuat(quat)
        green_line.setHpr(hpr)
        blue_line.hprInterval(3, hpr).start()  # 待测试
        yellow_line.quatInterval(6, quat).start()  # 待测试

    def HprAndQuat(self):
        """
        测试是否能够通过quat计算出正确的hpr值
        """
        white_line = self.drawLine([0, 0, 0], [3, 6, 9], self.render)
        red_line = self.drawLine([0, 0, 0], [0, 0, 3], self.render, color=(1, 0, 0, 1))

        vec = [1, 2, 3]

        # 这种方式计算得到的Quat应用到红线后，可以观察到没有和白线重合，说明计算仍然不可用
        print(f"white_line hpr:{white_line.getHpr()}")
        quat = calcQuatFromVector(vec)
        print(quat)
        print(f"quat hpr:{quat.getHpr()}")
        red_line.setQuat(quat)

    def HprAndH_P_R(self):
        """
        测试hpr和h、p、r的关系
        """
        hpr = p3d.Vec3(53.300774799510116, 15.501359566936996, 32.311533237423845)
        h = p3d.Vec3(53.300774799510116, 0, 0)
        p = p3d.Vec3(0, 15.501359566936996, 0)
        r = p3d.Vec3(0, 0, 32.311533237423845)

        white_line = self.drawLine([0, 0, 0], [3, 6, 9], self.render)
        red_line = self.drawLine([0, 0, 0], [0, 0, 3], self.render, color=(1, 0, 0, 1))
        green_line = self.drawLine([0, 0, 0], [0, 0, 3], self.render, color=(0, 1, 0, 1))
        blue_line = self.drawLine([0, 0, 0], [0, 0, 3], self.render, color=(0, 0, 1, 1))
        # 绿色和蓝色的线重合，说明分开设置HPR和直接设置HPR是一样的
        green_line.setHpr(hpr)
        blue_line.setH(hpr[0])
        blue_line.setP(hpr[1])
        blue_line.setR(hpr[2])
        # 红色的线使用hprInterval来插值设置hpr，会发现位置不一致，说明hprInterval每次都是设置hpr三个值，所以不能分开设置h、p、r
        h_interval = red_line.hprInterval(5, h)
        p_interval = red_line.hprInterval(5, p)
        r_interval = red_line.hprInterval(5, r)
        Sequence(h_interval, p_interval, r_interval).start()
        # 绿色和蓝色的线与白色的线并没有重合，说明分开计算三个平面上的旋转角并不能得到正确的hpr值

    def drawLine(self, start, end, parent_node, color=(1, 1, 1, 1), thickness=5):
        # 创建LineSegs对象
        lines = LineSegs()
        # 设置线条的颜色和宽度
        lines.setColor(*color)  # 白色
        lines.setThickness(thickness)  # 宽度为2
        # 添加线条的顶点
        lines.moveTo(start[0], start[1], start[2])
        lines.drawTo(end[0], end[1], end[2])
        # 创建线条的节点
        node = lines.create()
        # 创建线条的GeomNode，并添加到场景中
        line_node = self.render.attachNewNode(node)
        return line_node

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


app = MyApp()
app.run()
