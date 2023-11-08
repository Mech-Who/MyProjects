import os
import sys

sys.path.append(r"D:\Project\MyProjects\FeatureExtraction")
sys.path.append(r"D:\Project\MyProjects\FeatureExtraction\DataAugmentation")

import DataAugmentation

root = "./python/dataset"
crop_image_path = f"{root}/crop"
color_vibrance_image_path = f"{root}/color_vibrance"
rotate_image_path = f"{root}/rotate"
shift_image_path = f"{root}/shift"
zoom_image_path = f"{root}/zoom"

paths = [
    crop_image_path,
    color_vibrance_image_path,
    rotate_image_path,
    shift_image_path,
    zoom_image_path
]

for path in paths:
    if not os.path.exists(path):
        os.mkdir(path)

image_count = 100

DataAugmentation.create_cropped_image(crop_image_path, count=image_count)
DataAugmentation.create_color_vibrance_image(color_vibrance_image_path, count=image_count)
DataAugmentation.create_rotate_image(rotate_image_path, count=image_count)
DataAugmentation.create_shift_image(shift_image_path, count=image_count)
DataAugmentation.create_zoom_image(zoom_image_path, count=image_count)

