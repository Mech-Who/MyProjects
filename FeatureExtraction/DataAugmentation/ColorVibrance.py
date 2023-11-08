import os
import random

import cv2
import numpy as np
import matplotlib.pyplot as plt

from PIL import ImageEnhance, Image
from utils import getFiles


def randomColor(image, saturation=0, brightness=0, contrast=0, sharpness=0):
    if random.random() < saturation:
        random_factor = np.random.randint(0, 31) / 10.  # 随机因子
        image = ImageEnhance.Color(image).enhance(random_factor)  # 调整图像的饱和度
    if random.random() < brightness:
        random_factor = np.random.randint(10, 21) / 10.  # 随机因子
        image = ImageEnhance.Brightness(
            image).enhance(random_factor)  # 调整图像的亮度
    if random.random() < contrast:
        random_factor = np.random.randint(10, 21) / 10.  # 随机因子
        image = ImageEnhance.Contrast(image).enhance(random_factor)  # 调整图像对比度
    if random.random() < sharpness:
        random_factor = np.random.randint(0, 31) / 10.  # 随机因子
        ImageEnhance.Sharpness(image).enhance(random_factor)  # 调整图像锐度
    return image

def create_color_vibrance_image(image_path, recursion=False, subdirname=None, count=1):
    """
    色彩抖动：饱和度，亮度，对比度，锐度
    image_path: 图片路径
    recursion: 是否递归搜索图片目录，默认为False，不进行递归搜索
    subdirname: 子目录名称
    count: 生成图片的数量
    """
    image_path = os.path.abspath(image_path)
    files = getFiles(image_path, recursion)
    for img_path in files:
        img = cv2.imread(img_path)
        # 原图
        cj_img = Image.fromarray(img)
        # 设置图片名
        filename = img_path.split("\\")[-1].split('.')[0]
        for i in range(int(count/5)):
            # 调整饱和度
            sa_img = np.asarray(randomColor(cj_img, saturation=1))
            # 调整亮度
            br_img = np.asarray(randomColor(cj_img, brightness=1))
            # 调整对比度
            co_img = np.asarray(randomColor(cj_img, contrast=1))
            # 调整锐度
            sh_img = np.asarray(randomColor(cj_img, sharpness=1))
            # 调整所有项
            rc_img = np.asarray(randomColor(cj_img, saturation=1,
                                            brightness=1, contrast=1, sharpness=1))
            new_saturation_filename = filename + f'_saturation{i+1:03d}.jpg'
            new_brightness_filename = filename + f'_brightness{i+1:03d}.jpg'
            new_contrast_filename = filename + f'_contrast{i+1:03d}.jpg'
            new_sharpness_filename = filename + f'_sharpness{i+1:03d}.jpg'
            new_random_color_filename = filename + f'_random_color{i+1:03d}.jpg'
            if subdirname:
                dir_name = os.path.join(image_path, subdirname)
                if not os.path.exists(dir_name):
                    os.mkdir(dir_name)
                saturation_img_path = os.path.join(dir_name, new_saturation_filename)
                brightness_img_path = os.path.join(dir_name, new_brightness_filename)
                contrast_img_path = os.path.join(dir_name, new_contrast_filename)
                sharpness_img_path = os.path.join(dir_name, new_sharpness_filename)
                random_color_img_path = os.path.join(dir_name, new_random_color_filename)
            else:
                saturation_img_path = os.path.join(image_path, new_saturation_filename)
                brightness_img_path = os.path.join(image_path, new_brightness_filename)
                contrast_img_path = os.path.join(image_path, new_contrast_filename)
                sharpness_img_path = os.path.join(image_path, new_sharpness_filename)
                random_color_img_path = os.path.join(image_path, new_random_color_filename)
            print(f"{saturation_img_path} has saved!")
            print(f"{brightness_img_path} has saved!")
            print(f"{contrast_img_path} has saved!")
            print(f"{sharpness_img_path} has saved!")
            print(f"{random_color_img_path} has saved!")
            # 保存图片
            cv2.imwrite(saturation_img_path, sa_img)
            cv2.imwrite(brightness_img_path, br_img)
            cv2.imwrite(contrast_img_path, co_img)
            cv2.imwrite(sharpness_img_path, sh_img)
            cv2.imwrite(random_color_img_path, rc_img)

if __name__ == "__main__":
    image_path = r"./DataAugmentation/TestImage/"
    # create_color_vibrance_image(image_path, None)
    create_color_vibrance_image(image_path, "color_vibrance")