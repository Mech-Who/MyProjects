import os
import sys

sys.path.append(r"D:\Project\MyProjects\FeatureExtraction")
sys.path.append(r"D:\Project\MyProjects\FeatureExtraction\DataAugmentation")

import DataAugmentation

# 设置数据集目录
root = "./python/dataset"

trans_type = ['crop', 'color_vibrance', 'rotate', 'shift', 'zoom']

paths = [f"{root}/{trans}" for trans in trans_type]

import random

source_path = './VOC2007/VOCdevkit/JPEGImages'
source_absolute_path = os.path.abspath(source_path)
files = DataAugmentation.utils.getFiles(source_absolute_path, False)
sources = random.choices(files, k=len(paths))

import shutil

# 创建目录
for path in paths:
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        shutil.rmtree(path)
        os.mkdir(path)

# 移动文件
for source, path in zip(sources, paths):
    shutil.copy(source, path)


# 生成增强图片
image_count = int(input("要生成的图片数量（整数）："))

for path, trans in zip(paths, trans_type):
    if trans == 'crop':
        DataAugmentation.create_cropped_image(path, count=image_count)
    elif trans == 'color_vibrance':
        DataAugmentation.create_color_vibrance_image(path, count=image_count)
    elif trans == 'rotate':
        DataAugmentation.create_rotate_image(path, count=image_count)
    elif trans == 'shift':
        DataAugmentation.create_shift_image(path, count=image_count)
    elif trans == 'zoom':
        DataAugmentation.create_zoom_image(path, count=image_count)

