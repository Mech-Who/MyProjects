# 去除黑边的操作
import os
import cv2
import random
import matplotlib.pyplot as plt
import numpy as np

from utils import getFiles

crop_image = lambda img, x0, y0, w, h: img[y0:y0+h, x0:x0+w]  # 定义裁切函数，后续裁切黑边使用

def rotate_image(img, angle, crop):
    """
    angle: 旋转的角度
    crop: 是否需要进行裁剪，布尔向量
    """
    w, h = img.shape[:2]
    # 旋转角度的周期是360°
    angle %= 360
    # 计算仿射变换矩阵
    M_rotation = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1)
    # 得到旋转后的图像
    img_rotated = cv2.warpAffine(img, M_rotation, (w, h))

    # 如果需要去除黑边
    if crop:
        # 裁剪角度的等效周期是180°
        angle_crop = angle % 180
        if angle > 90:
            angle_crop = 180 - angle_crop
        # 转化角度为弧度
        theta = angle_crop * np.pi / 180
        # 计算高宽比
        hw_ratio = float(h) / float(w)
        # 计算裁剪边长系数的分子项
        tan_theta = np.tan(theta)
        numerator = np.cos(theta) + np.sin(theta) * np.tan(theta)

        # 计算分母中和高宽比相关的项
        r = hw_ratio if h > w else 1 / hw_ratio
        # 计算分母项
        denominator = r * tan_theta + 1
        # 最终的边长系数
        crop_mult = numerator / denominator

        # 得到裁剪区域
        w_crop = int(crop_mult * w)
        h_crop = int(crop_mult * h)
        x0 = int((w - w_crop) / 2)
        y0 = int((h - h_crop) / 2)
        img_rotated = crop_image(img_rotated, x0, y0, w_crop, h_crop)
    return img_rotated

def create_rotate_image(image_path, subdirname=None, count=1):
    image_path = os.path.abspath(image_path)
    files = getFiles(image_path)
    for img_path in files:
        img = cv2.imread(img_path)
        for i in range(count):
            # 随机旋转度数
            degree = random.randint(0, 360)
            # 无黑边旋转
            nonblack_image_rotated = rotate_image(img, degree, True)
            # 有黑边旋转
            black_image_rotated = rotate_image(img, degree, False)
            # 保存图片
            filename = img_path.split("\\")[-1].split('.')[0]
            new_black_filename = filename + f'_black{degree:03d}rotate{i+1:03d}.jpg'
            new_nonblack_filename = filename + f'_nonblack{degree:03d}rotate{i+1:03d}.jpg'
            if subdirname:
                new_black_img_path = os.path.join(image_path, subdirname, new_black_filename)
                new_nonblack_img_path = os.path.join(image_path, subdirname, new_nonblack_filename)
            else:
                new_black_img_path = os.path.join(image_path, new_black_filename)
                new_nonblack_img_path = os.path.join(image_path, new_nonblack_filename)
            print(f"{new_black_img_path} has saved!")
            print(f"{new_nonblack_img_path} has saved!")
            # cv2.imwrite(new_black_img_path, black_image_rotated)
            # cv2.imwrite(new_nonblack_img_path, nonblack_image_rotated)

if __name__ == "__main__":
    image_path = r"./DataAugmentation/TestImage"
    create_rotate_image(image_path, "rotate", 2)
    create_rotate_image(image_path, None, 2)
