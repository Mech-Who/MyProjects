import cv2
import matplotlib as plt
import numpy as np

mat_shift = np.float32([[1, 0, 100], [0, 1, 200]])
img_1 = cv2.warpAffine(img, mat_shift, (h, w))
mat_shift = np.float32([[1, 0, -150], [0, 1, -150]])
img_2 = cv2.warpAffine(img, mat_shift, (h, w))

# 显示
plt.figure(figsize=(15, 10))
plt.subplot(1, 3, 1), plt.imshow(img)
plt.axis('off')
plt.title('原图')
plt.subplot(1, 3, 2), plt.imshow(img_1)
plt.axis('off')
plt.title('向右下移动')
plt.subplot(1, 3, 3), plt.imshow(img_2)
plt.axis('off')
plt.title('左上移动')
plt.show()
