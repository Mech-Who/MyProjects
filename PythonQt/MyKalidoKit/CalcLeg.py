import panda3d.core as p3d
from MyKalidoKit.Util.Helper import calcMiddleAngle, getRotationFromVector, makeVecFromHpr, lerpVector


def calcLeg(leg, lm3d, end_key, start_key, third_key):
    """
    根据mediapipe所提供的landmarks来计算手臂的旋转
    :param leg: 关节对象
    :param lm3d: landmarks的手臂值
    :param end_key: mediapipe中的骨骼终点
    :param start_key: mediapipe中的骨骼起点
    :param third_key: mediapipe中用于计算骨骼夹角的第三个点
    :return: dict
    """
    first_vec = p3d.Vec3(lm3d[third_key].x, lm3d[third_key].y, lm3d[third_key].z)
    second_vec = p3d.Vec3(lm3d[start_key].x, lm3d[start_key].y, lm3d[start_key].z)
    third_vec = p3d.Vec3(lm3d[end_key].x, lm3d[end_key].y, lm3d[end_key].z)
    # 指定的全局坐标系中的向量方向
    target_vector = p3d.Vec3(lm3d[end_key].x-lm3d[start_key].x,
                             lm3d[end_key].y-lm3d[start_key].y,
                             lm3d[end_key].z-lm3d[start_key].z)
    # 获得骨骼当前的方向向量
    current_global_transform = leg.getTransform()
    current_hpr = current_global_transform.getHpr()
    current_vector = makeVecFromHpr(current_hpr[0], current_hpr[1], current_hpr[2])
    # 获得hpr值或者quat值
    rotation_hpr, rotation_quat = getRotationFromVector(current_vector, target_vector)
    # 重新计算P值，因为上面获得的p值无法让手臂前后摇摆
    degree = calcMiddleAngle(first_vec, second_vec, third_vec)
    # 先应用H和R值
    leg.setQuat(leg.getQuat() * rotation_quat)
    # 再应用P值
    # leg.setHpr(leg.getH(), leg.getP()+degree, leg.getR())
