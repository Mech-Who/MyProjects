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
    strMethod = ["SIFT", "SURF", "BRISK", "ORB", "AKAZE"]
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
                    # extractor = cv2.xfeaturees2d.SIFT_create()
                    extractor = cv2.SIFT.create()
                    matcher = cv2.BFMatcher(cv2.NORM_L2)
                elif imethod == 1:  # "SURF"
                    extractor = cv2.xfeaturees2d.SURF_create()
                    # extractor= cv2.SURF.create()
                    cv2.SURF
                    matcher = cv2.BFMatcher(cv2.NORM_L2)
                elif imethod == 2:  # "BRISK"
                    # extractor = cv2.xfeaturees2d.BRISK_create()
                    extractor = cv2.BRISK.create()
                    matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
                elif imethod == 3:  # "ORB"
                    # extractor= cv2.xfeaturees2d.ORB_create()
                    extractor = cv2.ORB.create()
                    matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
                elif imethod == 4:  # "AKAZE"
                    # extractor= cv2.xfeaturees2d.AKAZE_create()
                    extractor = cv2.AKAZE.create()
                    matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
                try:
                    extractor.detectAndCompute(
                        img1, np.ndarray, keypoints1, descriptors1)
                    extractor.detectAndCompute(
                        imgn, np.ndarray, keypoints2, descriptors2)
                    matcher.match(descriptors1, descriptors2, matches)
                except Exception as e:
                    print(" 特征点提取时发生错误 ")
                    continue
                # 对特征点进行粗匹配
                max_dist = 0.0
                min_dist = 100.0
                for a in range(matches.size()):
                    dist = matches[a].distance
                    if (dist < min_dist):
                        min_dist = dist
                    if (dist > max_dist):
                        max_dist = dist
                for a in range(matches.size()):
                    if (matches[a].distance <= max(2*min_dist, 0.02)):
                        good_matches.push_back(matches[a])
                if (good_matches.size() < 4):
                    print(" 有效特征点数目小于4个，粗匹配失败 ")
                    continue
                # 通过RANSAC方法，对现有的特征点对进行“提纯”
                obj = [(0, 0)]
                scene = [(0, 0)]
                for a in range(int(good_matches.size())):
                    # 分别将两处的good_matches对应的点对压入向量,只需要压入点的信息就可以
                    obj.push_back(keypoints1[good_matches[a].queryIdx].pt)
                    scene.push_back(keypoints2[good_matches[a].trainIdx].pt)
                # 计算单应矩阵（在calib3d中)
                H = np.zeros([0])
                try:
                    H = cv2.findHomography(obj, scene, cv2.CV_RANSAC)
                except Exception as e:
                    print(" findHomography失败 ")
                    continue
                if (H.rows < 3):
                    print(" findHomography失败 ")
                    continue
                # 计算内点数目
                matObj = np.zeros([0])
                matScene = np.zeros([0])
                # TODO: data.db不存在
                pcvMat = H
                Hmodel = pcvMat.data.db
                Htmp = Hmodel[6]
                for isize in range(obj.size()):
                    ww = 1./(Hmodel[6]*obj[isize].x +
                             Hmodel[7]*obj[isize].y + 1.)
                    dx = (Hmodel[0]*obj[isize].x + Hmodel[1] *
                          obj[isize].y + Hmodel[2])*ww - scene[isize].x
                    dy = (Hmodel[3]*obj[isize].x + Hmodel[4] *
                          obj[isize].y + Hmodel[5])*ww - scene[isize].y
                    err = float(dx*dx + dy*dy)  # 3个像素之内认为是同一个点
                    if (err < 9):
                        innersize += 1
                # 打印内点占全部特征点的比率
                ff = float(innersize) / float(good_matches.size())
                print(ff)
                # 打印时间
                print(f" {(cv2.getTickCount() - t) / cv2.getTickFrequency()}")
                t = cv2.getTickCount()
                # 如果效果较好，则打印出来
                matTmp = np.zeros([0])
                if (ff == 1.0):
                    cv2.drawMatches(img1, keypoints1, imgn,
                                    keypoints2, good_matches, matTmp)
                    charJ = iimage
                    strResult = results + \
                        strDateset[idateset] + _strMethod + charJ
                    cv2.imwrite(strResult, matTmp)
                ff = 0
                innersize = 0
                matches.clear()
                good_matches.clear()
            files.clear()
    input()
    cv2.waitKey()
    return


if __name__ == "__main__":
    main()
