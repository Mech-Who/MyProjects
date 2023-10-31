import cv2
import numpy as np


if __name__ == "__main__":

    # 打开摄像头
    cap = cv2.VideoCapture(0)

    # 调整亮度和对比度
    alpha = 0.8  # 增强倍数
    beta = 50  # 增强偏移量

    while True:
        # 读取帧
        ret, frame = cap.read()

        # 对图像进行亮度和对比度调整
        frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

        # 转换颜色空间
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)

        # 中值滤波
        frame = cv2.medianBlur(frame, 3)  # 画面平滑
        # frame = cv2.GaussianBlur(frame, (3, 3), 0)  # 画面模糊
        # frame = cv2.Canny(frame, 50, 150)  # 只显示边缘

        # 显示帧
        cv2.imshow('frame', frame)

        # 退出键
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放摄像头
    cap.release()

    # 关闭窗口
    cv2.destroyAllWindows()

