# third-party library
import cv2
import mediapipe as mp

# standard library
from collections import namedtuple

# custom library
from testPanda3D import MyApp

#  配置mediapipe的holistic算法
mp_holistic = mp.solutions.holistic
drawing = mp.solutions.drawing_utils

Landmark = namedtuple('Landmark', ['x', 'y', 'z', 'visibility'])

def draw_points(image, results):
    # 绘制人脸关键点
    # drawing.draw_landmarks(
    #     image,
    #     results.face_landmarks,
    #     mp_holistic.FACEMESH_CONTOURS)

    # 绘制人体关键点
    drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_holistic.POSE_CONNECTIONS)

    # 绘制左手关键点
    # drawing.draw_landmarks(
    #     image,
    #     results.left_hand_landmarks,
    #     mp_holistic.HAND_CONNECTIONS)

    # 绘制右手关键点
    # drawing.draw_landmarks(
    #     image,
    #     results.right_hand_landmarks,
    #     mp_holistic.HAND_CONNECTIONS)


def save_data(results):
    with open("./results/pose_world_landmarks.txt", 'w') as f:
        for i, lm in enumerate(results.pose_world_landmarks.landmark):
            f.write(f"{i}:\n{lm}\n")
    with open("./results/pose_landmarks.txt", 'w') as f:
        for i, lm in enumerate(results.pose_landmarks.landmark):
            f.write(f"{i}:\n{lm}\n")
    with open("./results/left_hand_landmarks.txt", 'w') as f:
        for i, lm in enumerate(results.left_hand_landmarks.landmark):
            f.write(f"{i}:\n{lm}\n")
    with open("./results/right_hand_landmarks.txt", 'w') as f:
        for i, lm in enumerate(results.right_hand_landmarks.landmark):
            f.write(f"{i}:\n{lm}\n")
    with open("./results/face_landmarks.txt", 'w') as f:
        for i, lm in enumerate(results.face_landmarks.landmark):
            f.write(f"{i}:\n{lm}\n")


if __name__ == '__main__':
    with mp_holistic.Holistic(static_image_mode=False,
                              min_detection_confidence=0.7,
                              min_tracking_confidence=0.7
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

        # 3.原图绘制关键点
        draw_points(image, results)

        # 3.1 提取关键点坐标数据
        # 保存坐标数据到文件
        # height, width, color = image.shape
        # save_data(results)

        # 3.2 根据BlazePose谷歌模型的关键点划分，划分数据
        # 元素通过pose_coords[0].x、pose_coords[0].y、pose_coords[0].z和pose_coords[0].visibility访问
        # pose_world_coords = [[lm.x, lm.z, -lm.y] for lm in results.pose_world_landmarks.landmark]
        scale_factor = 1
        pose_world_coords = [Landmark(x=lm.x*scale_factor, y=lm.z*scale_factor, z=-lm.y*scale_factor, visibility=lm.visibility) for lm in results.pose_world_landmarks.landmark]
        pose_coords = [Landmark(x=lm.x*scale_factor, y=lm.z*scale_factor, z=-lm.y*scale_factor, visibility=lm.visibility) for lm in results.pose_landmarks.landmark]
        # pose_world_coords = [lm for lm in results.pose_world_landmarks.landmark]
        # pose_coords = [lm for lm in results.pose_landmarks.landmark]
        # left_hand_coords = np.array([[lmk.x, lmk.z, -lmk.y] for lmk in results.left_hand_landmarks.landmark])
        # right_hand_coords = np.array([[lmk.x, lmk.z, -lmk.y] for lmk in results.right_hand_landmarks.landmark])
        # face_coords = np.array([[lmk.x, lmk.z, -lmk.y] for lmk in results.face_landmarks.landmark])

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imshow("image", image)

        # 3.3 查找骨骼映射
        app = MyApp()
        app.setFrame(pose_world_coords, pose_coords)
        app.run()

        # 4.OpenCV展示
        # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # cv2.imshow("image", image)

        key = cv2.waitKey(0)
        if key & 0xFF == 'q':
            exit(0)
