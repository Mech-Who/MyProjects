import random
import numpy as np
import matplotlib as plt
from PIL import ImageEnhance, Image


def randomColor(image, saturation=0, brightness=0, contrast=0, sharpness=0):
    if random.random() < saturation:
        random_factor = np.random.randint(0, 31) / 10.  # 随机因子
        image = ImageEnhance.Color(image).enhance(random_factor)  # 调整图像的饱和度
    if random.random() < brightness:
        random_factor = np.random.randint(10, 21) / 10.  # 随机因子
        image = ImageEnhance.Brightness(
            image).enhance(random_factor)  # 调整图像的亮度
    if random.random() < contrast:
        random_factor = np.random.randint(10, 21) / 10.  # 随机因1子
        image = ImageEnhance.Contrast(image).enhance(random_factor)  # 调整图像对比度
    if random.random() < sharpness:
        random_factor = np.random.randint(0, 31) / 10.  # 随机因子
        ImageEnhance.Sharpness(image).enhance(random_factor)  # 调整图像锐度
    return image


cj_img = Image.fromarray(img)
sa_img = np.asarray(randomColor(cj_img, saturation=1))
br_img = np.asarray(randomColor(cj_img, brightness=1))
co_img = np.asarray(randomColor(cj_img, contrast=1))
sh_img = np.asarray(randomColor(cj_img, sharpness=1))
rc_img = np.asarray(randomColor(cj_img, saturation=1,
                                brightness=1, contrast=1, sharpness=1))
plt.figure(figsize=(15, 10))
plt.subplot(2, 3, 1), plt.imshow(img)
plt.axis('off')
plt.title('原图')
plt.subplot(2, 3, 2), plt.imshow(sa_img)
plt.axis('off')
plt.title('调整饱和度')
plt.subplot(2, 3, 3), plt.imshow(br_img)
plt.axis('off')
plt.title('调整亮度')
plt.subplot(2, 3, 4), plt.imshow(co_img)
plt.axis('off')
plt.title('调整对比度')
plt.subplot(2, 3, 5), plt.imshow(sh_img)
plt.axis('off')
plt.title('调整锐度')
plt.subplot(2, 3, 6), plt.imshow(rc_img)
plt.axis('off')
plt.title('调整所有项')
plt.show()
