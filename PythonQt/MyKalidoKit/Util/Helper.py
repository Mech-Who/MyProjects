import panda3d.core as p3d


def getRotationFromVector(from_vec, to_vec):
    """
    获得从from_vec到to_vec的旋转hpr值或者quat值
    :param from_vec: 旋转开始位置的向量
    :param to_vec: 旋转结束位置的向量
    :return: hpr值或quat值
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


def makeVecFromHpr(h, p, r):
    """
    根据已知的hpr值得到指向该方向的单位向量
    :param h: h值
    :param p: p值
    :param r: r值
    :return: 指向该方向的单位向量
    """
    # 已知的HPR角度
    hpr = p3d.Vec3(h, p, r)
    direction_transform = p3d.TransformState.makeHpr(hpr)
    rotation_matrix = direction_transform.getMat()

    # 构造单位向量
    unit_vector = p3d.Vec3(1.0, 0.0, 0.0)  # 示例中假设方向为 x 轴正方向
    rotated_vector = rotation_matrix.xform(unit_vector)
    return rotated_vector


def calcMiddleAngle(vec_a, vec_b, vec_c):
    """
    计算a,b,c三点的夹角
    :param vec_a: 点a的vec
    :param vec_b: 点b的vec
    :param vec_c: 点c的vec
    :return: 夹角角度
    """
    # 计算夹角向量
    vec1 = vec_a - vec_b
    vec2 = vec_c - vec_b
    # 归一化
    vec1 = vec1.normalized()
    vec2 = vec2.normalized()
    # 调用函数计算夹角
    degree = vec1.angleDeg(vec2)
    return degree


def lerpVector(first_vec, second_vec, fraction):
    """
    根据fraction获得夹在first_vec和second_vec间的向量
    :param first_vec: 第一个向量
    :param second_vec: 第二个向量
    :param fraction: 中间分数，即要这两个向量中间哪个位置的向量
    :return: 中间向量
    """
    add_vec = first_vec - second_vec
    add_vec *= fraction
    final_vec = second_vec + add_vec
    return final_vec
