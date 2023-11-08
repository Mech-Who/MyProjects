import os
import sys

sys.path.append(r"D:\Project\MyProjects\FeatureExtraction")

import DataAugmentation



crop_image_path = "./python/crop"
color_vibrance_image_path = "./python/color_vibrance"
rotate_image_path = "./python/rotate"
shift_image_path = "./python/shift"
zoom_image_path = "./python/zoom"

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

