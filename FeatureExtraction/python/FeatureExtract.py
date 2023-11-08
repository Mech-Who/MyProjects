import numpy as np
import cv2
import os


root = "D:/Project/MyProjects/FeatureExtraction/python"
dataset = f"{root}/dataset/"
results = f"{root}/results.txt"


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


def writeFileAndPrint(filename, message, mode='a', encoding='utf-8'):
    print(message)
    with open(filename, mode=mode, encoding=encoding) as f:
        f.write(message)
        f.write('\n')


def select_method(choose):
    """根据数字选方法，返回executor和matcher"""
    extractor = ''
    matcher = ''
    if choose == 0:  # "SIFT"
        extractor = cv2.SIFT_create()
        matcher = cv2.BFMatcher(cv2.NORM_L2)
    elif choose == 1:  # "BRISK"
        extractor = cv2.BRISK.create()
        matcher = cv2.BFMatcher(cv2.NORM_L2)
    elif choose == 2:  # "ORB"
        extractor = cv2.ORB.create()
        matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
    elif choose == 3:  # "AKAZE"
        extractor = cv2.AKAZE.create()
        matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
    return (extractor, matcher)


def process_data(basic_file: str, current_file: str, 
                 extractor: cv2.Feature2D, matcher: cv2.BFMatcher):
    """
    处理数据：
    1. 提取特征点
    2. 特征点匹配
    3. 内点提取

    """
    # 使用img1对比余下的图片，得出结果
    img1 = cv2.imread(basic_file, 0)
    imgn = cv2.imread(current_file, 0)

    # 错读数据
    delta_error_read = 0

    # 提取特征点
    query_keypoints, train_keypoints = 0, 0
    matches = []
    try:
        query_keypoints, query_descriptors = extractor.detectAndCompute(img1, None)
        train_keypoints, train_descriptors = extractor.detectAndCompute(imgn, None)
        matches = matcher.match(query_descriptors, train_descriptors)
    except Exception as e:
        print(" 特征点提取时发生错误 ")
        delta_error_read += 1
        return 0, delta_error_read

    # 对特征点进行粗匹配
    max_dist = 0.0
    min_dist = 100.0
    for match in matches:
        dist = match.distance
        if (dist < min_dist):
            min_dist = dist
        if (dist > max_dist):
            max_dist = dist

    good_matches = [match for match in matches if match.distance <= max(2 * min_dist, 0.02)]

    # 粗匹配原本是要求4个特征点
    # 粗匹配先过滤一部分特征点
    if (len(good_matches) < 4):
        print(" 有效特征点数目小于4个，粗匹配失败 ")
        delta_error_read += 1
        return 0, delta_error_read

    # # 使用RANSAC进行内点提纯
    # points1, points2 = [], []  # cv2.typing.Point2f
    # for good in good_matches:
    #     queryIdx = good.queryIdx
    #     trainIdx = good.trainIdx

    #     if queryIdx >= 0 and queryIdx < len(query_keypoints) \
    #             and trainIdx >= 0 and trainIdx < len(train_keypoints):
    #         points1.append(query_keypoints[queryIdx].pt)
    #         points2.append(train_keypoints[trainIdx].pt)
    
    matched_points = [(query_keypoints[match.queryIdx].pt, train_keypoints[match.trainIdx].pt) for match in good_matches]

    src_points = np.float32([m[0] for m in matched_points])
    dst_points = np.float32([m[1] for m in matched_points])

    model, inliers = cv2.findHomography(src_points, dst_points, cv2.RANSAC, 1)

    refined_matched_points = [matched_points[i] for i in inliers.ravel()]

    if refined_matched_points == 0:
        print("无可用提纯点，提纯失败")
        delta_error_read += 1

    # # 通过RANSAC方法，对现有的特征点对进行“提纯”
    # obj, scene = [], []
    # for good in good_matches:
    #     # 分别将两处的good_matches对应的点对压入向量,只需要压入点的信息就可以
    #     obj.append(query_keypoints[good.queryIdx].pt)
    #     scene.append(train_keypoints[good.trainIdx].pt)

    # # 使用基础矩阵作为提纯模型
    # inliers_mask = np.zeros([5, 10])
    # F, inliers_mask = cv2.findFundamentalMat(
    #     np.array(points1), np.array(points2), cv2.FM_RANSAC, 0.0001, 0.99)

    # ransac_matches = []  # cv2.DMatch # 提纯之后的内点
    # iii = 0
    # for good in good_matches:
    #     if inliers_mask is not None and inliers_mask[iii] is not None and iii < inliers_mask.shape[0]:
    #         ransac_matches.append(good)
    #     iii += 1

    # if len(ransac_matches) == 0:
    #     delta_error_read += 1

    ff = float(len(refined_matched_points)) / len(good_matches)
    # print(f"ff: {ff}, float(innersize): {float(len(ransac_matches))}, len: {len(good_matches)}")

    return ff, delta_error_read


def main():
    strDataset = []
    for dataset_name in os.listdir(dataset):
        strDataset.append(dataset_name)
    strMethod = ["SIFT", "BRISK", "ORB", "AKAZE"]
    start_time = cv2.getTickCount()

    writeFileAndPrint(results, "SIFT、SURF、BRISK、ORB、AKAZE算法测试实验开始", mode='w')

    # 遍历各种特征点寻找方法
    for imethod in range(len(strMethod)):
        _strMethod = strMethod[imethod]
        writeFileAndPrint(results, f"===== 开始测试{strMethod[imethod]}方法 =====")

        # 遍历各个路径
        for idataset in range(len(strDataset)):
            # 获得测试图片绝对地址
            path = dataset + strDataset[idataset]
            writeFileAndPrint(results, f"== 开始测试数据集{strDataset[idataset]} ==")
            # 获得当前数据集中的图片,递归读取当前目录下全部图片
            files = getFiles(path)
            image_nums = len(files)
            writeFileAndPrint(results, f" 共{len(files)}张图片")

            # 生成特征点算法及其匹配方法
            extractor, matcher = select_method(imethod)

            # average_precision: 计算平均准确率
            # error_read: 算法能在多少张图像上匹配出最低数目的关键点
            average_precision, error_read = 0.0, 0
            for iimage in range(1, len(files)):
                print(f"开始处理第{iimage}张图片")
                delta_ap, delta_er = process_data(files[0], files[iimage], extractor, matcher)
                average_precision += delta_ap
                error_read += delta_er
            # 打印算法用时
            avg_time = ((cv2.getTickCount() - start_time) / cv2.getTickFrequency()) / 10
            writeFileAndPrint(results, f"算法平均用时：{avg_time}s/张")
            # 计算算法使用了多少张图像
            valid_image_num = image_nums - error_read
            writeFileAndPrint(results, f"用图数目: {valid_image_num}")
            # 平均准确率
            try:
                average_precision /= (image_nums - error_read)
                writeFileAndPrint(results, f"平均准确率: {average_precision}")
            except ZeroDivisionError as e:
                writeFileAndPrint(results, f"没有获得提取结果较好的图片:{e}")
            writeFileAndPrint(results, f"== 数据集{strDataset[idataset]}测试结束 ==")
        writeFileAndPrint(results, f"========== {strMethod[imethod]}方法测试结束 ==========")
    writeFileAndPrint(results, "实验结束")
    cv2.waitKey(0)
    return


if __name__ == "__main__":
    main()
