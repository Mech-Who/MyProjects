import os
import random
import cv2
import matplotlib.pyplot as plt
import numpy as np

from utils import getFiles

def create_zoom_image(image_path, recursion=False, subdirname=None, count=1):
    """
    image_path: 图片路径
    recursion: 是否递归搜索图片目录，默认为False，不进行递归搜索
    subdirname: 子目录名称
    count: 生成图片的数量
    """
    image_path = os.path.abspath(image_path)
    files = getFiles(image_path, recursion)
    for img_path in files:
        img = cv2.imread(img_path)
        h, w, ch = img.shape
        for i in range(count):
            # 图片缩放（0.25~2倍）
            zoom_h = int(h * (2 ** (random.random()*4 - 2)))
            zoom_w = int(w * (2 ** (random.random()*4 - 2)))

            zoom_img = cv2.resize(img, (zoom_w, zoom_h))
            # 保存图片
            filename = img_path.split("\\")[-1].split('.')[0]
            new_filename = filename + f'_zoom{i+1:03d}.jpg'
            if subdirname:
                dir_name = os.path.join(image_path, subdirname)
                if not os.path.exists(dir_name):
                    os.mkdir(dir_name)
                new_img_path = os.path.join(dir_name, new_filename)
            else:
                new_img_path = os.path.join(image_path, new_filename)
            print(f"{new_img_path} has saved!")
            cv2.imwrite(new_img_path, zoom_img)

if __name__ == "__main__":
    image_path = r"./DataAugmentation/TestImage"
    create_zoom_image(image_path, "zoom", 2)
    # create_zoom_image(image_path, None, 2)

# 显示
# plt.figure(figsize=(15, 10))
# plt.subplot(1, 3, 1), plt.imshow(img)
# plt.axis('off')
# plt.title('origin')
# plt.subplot(1, 3, 2), plt.imshow(img_2)
# plt.axis('off')
# plt.title('zoom out')
# plt.subplot(1, 3, 3), plt.imshow(img_3)
# plt.axis('off')
# plt.title('zoom in')
# plt.show()
