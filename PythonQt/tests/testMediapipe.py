import time

import cv2
import open3d
import numpy as np
import mediapipe as mp

mp_holistic = mp.solutions.holistic

holistic = mp_holistic.Holistic(static_image_mode=False,
        model_complexity=1,
        smooth_landmarks=True,
        # enable_segmentation=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
)
drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

point_x = []
point_y = []
point_z = []


# 提取x,y,z坐标
def get_x_y_z(each):
    point_x.append(each.x)
    point_y.append(each.y)
    point_z.append(each.z)
    return point_x, point_y, point_z


if __name__ == '__main__':
    t0 = time.time()
    cv2.namedWindow("video")
    capture = cv2.VideoCapture(0)
    while True:
        ret, frame = capture.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = holistic.process(frame)
        # 绘制人脸关键点
        drawing.draw_landmarks(
            frame,
            results.face_landmarks,
            mp_holistic.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_contours_style())
        # 绘制人体关键点
        drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_holistic.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles
            .get_default_pose_landmarks_style())
        # 绘制左手关键点
        drawing.draw_landmarks(
            frame,
            results.left_hand_landmarks,
            mp_holistic.HAND_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles
            .get_default_pose_landmarks_style())
        # 绘制右手关键点
        drawing.draw_landmarks(
            frame,
            results.right_hand_landmarks,
            mp_holistic.HAND_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles
            .get_default_pose_landmarks_style())
        coords = np.array(results.pose_landmarks.landmark)

        for index, each in enumerate(coords):
            x, y, z = get_x_y_z(each)
            # print("x: {}, y: {}, z:{}".format(x, y, z))
            point = np.vstack((x, y, z)).T
            print("FPS: {}".format(str(int(1 / (time.time() - t0)))))
            print(point)
            # 三维显示
            # point_cloud = open3d.geometry.PointCloud()
            # points = open3d.utility.Vector3dVector(point)
            # point_cloud.points = points
            # open3d.visualization.draw_geometries([point_cloud], window_name="video", width=640, height=480)
        cv2.imshow("video", frame)
        key = cv2.waitKey(1)
        if key & 0xFF == 'q':
            break