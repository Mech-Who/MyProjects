# 去除黑边的操作
import cv2
import matplotlib as plt
import numpy as np

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


#水平镜像
h_flip = cv2.flip(img,1)
#垂直镜像
v_flip = cv2.flip(img,0)
#水平垂直镜像
hv_flip = cv2.flip(img,-1)
#90度旋转
rows, cols, _ = img.shape
M = cv2.getRotationMatrix2D((cols/2, rows/2), 45, 1)
rotation_45 = cv2.warpAffine(img, M, (cols, rows))
#45度旋转
M = cv2.getRotationMatrix2D((cols/2, rows/2), 135, 2)
rotation_135 = cv2.warpAffine(img, M,(cols, rows))
#去黑边旋转45度
image_rotated = rotate_image(img, 45, True)

#显示
plt.figure(figsize=(15, 10))
plt.subplot(2,3,1), plt.imshow(img)
plt.axis('off'); plt.title('原图')
plt.subplot(2,3,2), plt.imshow(h_flip)
plt.axis('off'); plt.title('水平镜像')
plt.subplot(2,3,3), plt.imshow(v_flip)
plt.axis('off'); plt.title('垂直镜像')
plt.subplot(2,3,4), plt.imshow(hv_flip)
plt.axis('off'); plt.title('水平垂直镜像')
plt.subplot(2,3,5), plt.imshow(rotation_45)
plt.axis('off'); plt.title('旋转45度')
plt.subplot(2,3,6), plt.imshow(image_rotated)
plt.axis('off'); plt.title('去黑边旋转45度')
plt.show()