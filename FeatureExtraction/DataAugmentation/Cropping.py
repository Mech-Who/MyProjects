import cv2
import matplotlib as plt

img_path = '../../img/ch3_img1.jpg'
img = cv2.imread(img_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
h, w, _ = img.shape
new_h1, new_h2 = np.random.randint(0, h-512, 2)
new_w1, new_w2 = np.random.randint(0, w-512, 2)
img_crop1 = img[new_h1:new_h1+512, new_w1:new_w1+512, :]
img_crop2 = img[new_h2:new_h2+512, new_w2:new_w2+512, :]

# 显示
plt.figure(figsize=(15, 10))
plt.subplot(1,3,1), plt.imshow(img)
plt.axis('off'); plt.title('原图')
plt.subplot(1,3,2), plt.imshow(img_crop1)
plt.axis('off'); plt.title('水平镜像')
plt.subplot(1,3,3), plt.imshow(img_crop2)
plt.axis('off'); plt.title('垂直镜像')
plt.show()
