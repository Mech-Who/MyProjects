import os
import cv2
import numpy as np
from utils import getFiles

def random_crop(image, crop_size):
    height, width = image.shape[:2]
    crop_height, crop_width = crop_size
    if crop_width >= width or crop_height >= height:
        raise ValueError("Crop size should be smaller than image size")
    x = np.random.randint(0, width - crop_width + 1)
    y = np.random.randint(0, height - crop_height + 1)
    cropped_image = image[y:y+crop_height, x:x+crop_width]
    return cropped_image# 读取图像


def create_cropped_image(image_path, subdirname=None, crop_size=(200, 200), count=1):
    """
    image_path: 图片目录
    subdirname: 子目录名称
    crop_size: 裁剪尺寸
    count: 生成图片的数量
    """
    # 获取图片路径
    image_path = os.path.abspath(image_path)
    files = getFiles(image_path)
    for img_path in files:
        # 调整原图片大小
        image = cv2.imread(img_path)
        image = cv2.resize(image,(1024,800))
        # 随机裁剪到固定大小
        for i in range(count):
            cropped_image = random_crop(image, crop_size)# 显示原始图像和裁剪后的图像
            # 保存图片
            filename = img_path.split("\\")[-1].split('.')[0]
            new_filename = filename + f'_crop{i+1:03d}.jpg'
            if subdirname:
                new_img_path = os.path.join(image_path, subdirname, new_filename)
            else:
                new_img_path = os.path.join(image_path, new_filename)
            print(f"{new_img_path} has saved!")
            cv2.imwrite(new_img_path, cropped_image)


if __name__ == "__main__":
    image_path = r"./DataAugmentation/TestImage/"
    create_cropped_image(image_path, None, crop_size=(200, 200), count=2)
    create_cropped_image(image_path, "crop", crop_size=(200, 200), count=2)
