import kalidokit4python.Util.Vector as Vec
from kalidokit4python.Util.Vector import Vector
from kalidokit4python.Pose.PoseSolver import PoseSolver

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np


def plot_3d_coordinate_system(points, vectors):
    # 创建一个三维坐标系
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 提取点的坐标
    x = [point[0] for point in points]
    y = [point[1] for point in points]
    z = [point[2] for point in points]

    # 绘制点
    ax.scatter3D(x, y, z, c='red')

    for vector in vectors:
        # 提取向量的起点坐标和方向分量
        start_point, direction = vector
        vector_x, vector_y, vector_z = start_point
        vector_u, vector_v, vector_w = direction
        # 绘制向量
        ax.quiver(vector_x, vector_y, vector_z, vector_u, vector_v, vector_w)

    # 设置坐标轴标签
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # 提取所有坐标点
    all_points = points + [vector[0] for vector in vectors]

    # 计算坐标轴的范围
    min_x = min(point[0] for point in all_points)
    max_x = max(point[0] for point in all_points)
    min_y = min(point[1] for point in all_points)
    max_y = max(point[1] for point in all_points)
    min_z = min(point[2] for point in all_points)
    max_z = max(point[2] for point in all_points)

    max_axis = max([max_x, max_y, max_z])
    min_axis = max([min_x, min_y, min_z])

    # 设置坐标轴范围
    ax.set_xlim([min_axis, max_axis])
    ax.set_ylim([min_axis, max_axis])
    ax.set_zlim([min_axis, max_axis])

    # 自动缩放坐标轴
    ax.auto_scale_xyz([min_axis, max_axis], [min_axis, max_axis], [min_axis, max_axis])

    # 显示图形
    plt.show()


def calculate_rotation_angles(vector):
    # 计算向量在XY平面上的旋转角度
    xy_projection = np.sqrt(vector[0] ** 2 + vector[1] ** 2)
    xy_angle = np.arctan2(vector[2], xy_projection)

    # 计算向量在YZ平面上的旋转角度
    yz_projection = np.sqrt(vector[1] ** 2 + vector[2] ** 2)
    yz_angle = np.arctan2(vector[0], yz_projection)

    # 计算向量在ZX平面上的旋转角度
    zx_projection = np.sqrt(vector[2] ** 2 + vector[0] ** 2)
    zx_angle = np.arctan2(vector[1], zx_projection)

    return xy_angle, yz_angle, zx_angle


ps = [
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 2, 3)
]
vs = [
    (ps[0], (ps[1][0] - ps[0][0], ps[1][1] - ps[0][1], ps[1][2] - ps[0][2])),
    (ps[1], (ps[2][0] - ps[1][0], ps[2][1] - ps[1][1], ps[2][2] - ps[1][2])),
    (ps[2], (ps[0][0] - ps[2][0], ps[0][1] - ps[2][1], ps[0][2] - ps[2][2])),
    ((0, 0, 0), ps[3])
]
print(vs)
# vs = [(ps[i-1],
#             (ps[i][0] - ps[i-1][0], ps[i][1] - ps[i-1][1], ps[i][2] - ps[i-1][2]))
#            for i in range(len(ps))]
# print(vs)

plot_3d_coordinate_system(ps, vs)

origin = Vector(0, 0, 0)
pv = [Vector(p) for p in ps]

va = pv[1].subtract(pv[0])
vb = pv[2].subtract(pv[1])
vc = pv[0].subtract(pv[2])
vd = pv[3].subtract(origin)

print(f"result1: {Vector(*np.degrees(calculate_rotation_angles(va)))}")
print(f"result2: {Vector(*np.degrees(calculate_rotation_angles(vb)))}")
print(f"result3: {Vector(*np.degrees(calculate_rotation_angles(vc)))}")
print(f"result4: {Vector(*np.degrees(calculate_rotation_angles(vd)))}")

print()

result1 = Vec.findRotation(pv[0], pv[1])
result2 = Vec.findRotation(pv[1], pv[2])
result3 = Vec.findRotation(pv[2], pv[0])
result4 = Vec.findRotation(origin, pv[3])

print(f"result1:{result1.toDegree(180)}\nresult2:{result2.toDegree(180)}\n"
      f"result3:{result3.toDegree(180)}\nresult4:{result4.toDegree(180)}\n")
