"""
#include "stdafx.h"
#include <opencv2/core/utility.hpp>
#include "opencv2/imgproc.hpp"
#include "opencv2/videoio.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/calib3d.hpp"
#include "opencv2/xfeatures2d.hpp"
#include <iostream>
#include <ctype.h>
#include "GOCVHelper.h"

#define DATESET_COUNT 8
#define METHOD_COUNT 5

using namespace cv;
using namespace std;
using namespace xfeatures2d;
"""
import numpy as np
import cv2
import os

root = "D:/Project/MyProjects/FeatureExtraction"
dataset = f"{root}/dataset/"
results = f"{root}/results/"


def getFiles(directory_path):
    file_list = []

    # 遍历当前目录下的文件
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        if os.path.isfile(file_path):
            file_list.append(file_path)
        elif os.path.isdir(file_path):
            # 如果是子目录，递归调用该函数
            file_list.extend(getFiles(file_path))

    return file_list

# 遍历dateset,分别对SIFT, SURF, BRISK, ORB, FREAK算法进行运算，得出初步结论


def main():
    strDateset = ["ablation", "blur", "light",
                  "rotation", "viewpoint", "zoom"]
    strMethod = ["SIFT", "BRISK", "ORB", "AKAZE"]
    # 递归读取目录下全部文件
    files = [""]
    descriptors1 = np.zeros([0])
    keypoints1 = [cv2.KeyPoint()]
    descriptors2 = np.zeros([0])
    keypoints2 = [cv2.KeyPoint()]
    matches = [cv2.DMatch()]
    good_matches = [cv2.DMatch()]
    # 用于模型验算
    innersize = 0
    img1 = np.zeros([0])
    imgn = np.zeros([0])
    t = cv2.getTickCount()

    print("SIFT、SURF、BRISK、ORB、AKAZE算法测试实验开始")

    # 遍历各种特征点寻找方法
    METHOD_COUNT = len(strMethod)
    for imethod in range(METHOD_COUNT-1, METHOD_COUNT):
        _strMethod = strMethod[imethod]
        print(f"开始测试{imethod + 1}方法")
        # 遍历各个路径
        DATESET_COUNT = len(strDateset)
        for idateset in range(DATESET_COUNT):
            average_precision = 0.0  # 计算平均准确率
            error_read = 0  # 算法能在多少张图像上匹配出最低数目的关键点
            # 获得测试图片绝对地址
            path = dataset + strDateset[idateset]
            print(f"数据集为{strDateset[idateset]}")
            # 获得当个数据集中的图片
            files = getFiles(path)
            print(f" 共{len(files)}张图片")
            for iimage in range(1, len(files)):
                # 使用img1对比余下的图片，得出结果
                img1 = cv2.imread(files[0], 0)
                imgn = cv2.imread(files[iimage], 0)
                # 生成特征点算法及其匹配方法
                extractor = ''
                matcher = ''
                if imethod == 0:  # "SIFT"
                    extractor = cv2.SIFT.create()
                    matcher = cv2.BFMatcher(cv2.NORM_L2)
                elif imethod == 1:  # "BRISK"
                    extractor = cv2.BRISK.create()
                    matcher = cv2.BFMatcher(cv2.NORM_L2)
                elif imethod == 2:  # "ORB"
                    extractor = cv2.ORB.create()
                    matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
                elif imethod == 3:  # "AKAZE"
                    extractor = cv2.AKAZE.create()
                    matcher = cv2.BFMatcher(cv2.NORM_HAMMING)

                try:
                    extractor.detectAndCompute(
                        img1, cv2.UMat(), keypoints1, descriptors1)
                    extractor.detectAndCompute(
                        imgn, cv2.UMat(), keypoints2, descriptors2)
                    matcher.match(descriptors1, descriptors2, matches)
                except Exception as e:
                    print(" 特征点提取时发生错误 ")
                    error_read += 1
                    continue

                # 对特征点进行粗匹配
                max_dist = 0.0
                min_dist = 100.0

                for a in range(len(matches)):
                    dist = matches[a].distance
                    if (dist < min_dist):
                        min_dist = dist
                    if (dist > max_dist):
                        max_dist = dist

                for a in range(len(matches)):
                    if (matches[a].distance <= max(2 * min_dist, 0.02)):
                        good_matches.append(matches[a])

                # 粗匹配原本是要求4个特征点
                if (len(good_matches) < 2):
                    print(" 有效特征点数目小于2个，粗匹配失败 ")
                    error_read += 1
                    continue

                # 使用RANSAC进行内点提纯
                points1, points2 = [], []  # cv2.typing.Point2f
                for match in good_matches:
                    queryIdx = match.queryIdx
                    trainIdx = match.trainIdx

                    if queryIdx >= 0 and queryIdx < len(keypoints1) \
                            and trainIdx >= 0 and trainIdx < len(keypoints2):
                        points1.append(keypoints1[queryIdx].pt)
                        points2.append(keypoints2[trainIdx].pt)

                # 通过RANSAC方法，对现有的特征点对进行“提纯”
                obj = [(0, 0)]
                scene = [(0, 0)]
                for a in range(len(good_matches)):
                    # 分别将两处的good_matches对应的点对压入向量,只需要压入点的信息就可以
                    obj.push_back(keypoints1[good_matches[a].queryIdx].pt)
                    scene.push_back(keypoints2[good_matches[a].trainIdx].pt)

                # 使用基础矩阵作为提纯模型
                inliers_mask = np.zeros([5, 10])
                fundamental_matrix = cv2.findFundamentalMat(
                    points1, points2, cv2.FM_RANSAC, 3, 0.99, inliers_mask)

                ransac_matches = []  # cv2.DMatch # 提纯之后的内点
                iii = 0
                for match in good_matches:
                    if iii < inliers_mask.shape[-2]:
                        ransac_matches.append(match)
                    iii += 1

                innersize = len(ransac_matches)
                if innersize == 0:
                    error_read += 1

                ff = float(innersize) / len(good_matches)
                average_precision += ff

                ff = 0
                innersize = 0
                matches.clear()
                good_matches.clear()

            # 打印算法用时
            print(
                f"算法平均用时：{((cv2.getTickCount() - t) / cv2.getTickFrequency()) / 10}s/张")
            # 计算算法使用了多少张图像
            print(f"用图数目: {10 - error_read}")
            # 平均准确率
            average_precision /= (10 - error_read)
            print(f"平均准确率: {average_precision}")
            files.clear()
    cv2.waitKey(0)
    return


if __name__ == "__main__":
    main()
