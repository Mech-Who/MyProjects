import matplotlib.pyplot as plt
import cv2
import os
import random

from pprint import pprint

# 读取数据集
root = './python/dataset'
root = os.path.abspath(root)
datasets = [os.path.join(root, name) for name in os.listdir(root)]

# 每个数据集要读取的图片
show_num = 5

# 读取图片路径
showcase = {}
for dataset in datasets:
    img_paths = os.listdir(dataset)
    start = random.randint(0, len(img_paths)-5)
    show_paths = [os.path.join(dataset, name) for name in img_paths[start:start+show_num]]
    showcase[os.path.basename(dataset)] = show_paths


# 创建一个包含多个子图的图形
fig, axes = plt.subplots(nrows=len(showcase), ncols=show_num, figsize=(12, 10))

row = 0
col = 0
for dataset, img_paths in showcase.items():
    axes[row, 0].set_ylabel(dataset)
    for path in img_paths:
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        axes[row, col].imshow(img)
        axes[row, col].axis('off')
        col += 1
    row += 1
    col = 0

plt.tight_layout()
plt.show()
