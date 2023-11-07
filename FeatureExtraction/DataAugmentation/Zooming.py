import cv2
import matplotlib as plt

img_2 = cv2.resize(img, (int(h * 1.5), int(w * 1.5)))
img_2 = img_2[int((h - 512) / 2): int((h + 512) / 2),
              int((w - 512) / 2): int((w + 512) / 2), :]
img_3 = cv2.resize(img, (512, 512))

# 显示
plt.figure(figsize=(15, 10))
plt.subplot(1, 3, 1), plt.imshow(img)
plt.axis('off')
plt.title('原图')
plt.subplot(1, 3, 2), plt.imshow(img_2)
plt.axis('off')
plt.title('向外缩放')
plt.subplot(1, 3, 3), plt.imshow(img_3)
plt.axis('off')
plt.title('向内缩放')
plt.show()
