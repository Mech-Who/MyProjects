#include <iostream>
#include <ctype.h>
#include <opencv2/core/utility.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/calib3d.hpp>
#include <opencv2/features2d.hpp>
#include <windows.h>
#define DATESET_COUNT 6
#define METHOD_COUNT 4  
using namespace cv;
using namespace std;

string root = "D:/Project/MyProjects/FeatureExtraction";

// 获取目录下的所有文件名
vector<string> get_img_files_dir(const string &directory)
{
    string pattern = directory + "/*.*";
    vector<string> file_paths;
    glob(pattern, file_paths, false);
    return file_paths;
}

int main()
{
    SetConsoleOutputCP(CP_UTF8);

    string strDatesets[DATESET_COUNT];
    strDatesets[0] = "blur";
    strDatesets[1] = "light";
    strDatesets[2] = "rotation";
    strDatesets[3] = "viewpoint";
    strDatesets[4] = "zoom";
    strDatesets[5] = "ablation";
    string strMethods[METHOD_COUNT];
    strMethods[0] = "SIFT";
    strMethods[1] = "BRISK";
    strMethods[2] = "ORB";
    strMethods[3] = "AKAZE";      

    // 递归读取目录下全部文件
    vector<string> files;
    Mat descriptors1, descriptors2;
    vector<KeyPoint> keypoints1, keypoints2;
    vector<DMatch> matches, good_matches;
    // 用于模型验算
    int innersize = 0;
    Mat img1, imgn;
    int64 t;

    for (int n = 0; n < DATESET_COUNT; n++)
    {
        // 遍历每一种数据集下的图片
        string strDateset = strDatesets[n];
        cout << "=================== Use " << strDateset << "dataset ===================" << endl;
        string path = root + "/dataset/" + strDateset;
        files = get_img_files_dir(path);

        for (int m = 0; m < METHOD_COUNT; m++)
        {
            string strMethod = strMethods[m];
            int error_read = 0; // 算法能在多少张图像上匹配出最低数目的关键点
            float ap = 0;       // 计算平均准确率

            cout << "============ The " << strMethod << " algorithm comparision start! ============" << endl;
            t = getTickCount();

            for (int i = 1; i < 11; i++)
            {

                img1 = imread(files[0], 1); // 读取彩色图
                imgn = imread(files[i], 1);
                // 生成特征点算法及其匹配方法
                Ptr<Feature2D> extractor;
                BFMatcher matcher;
                //  选择算法
                switch (m)
                {
                case 0: //"SIFT"
                    extractor = SIFT::create();
                    matcher = BFMatcher(NORM_L2);
                    break;
                case 1: //"BRISK"
                    extractor = BRISK::create();
                    matcher = BFMatcher(NORM_L2);
                    break;
                case 2: //"ORB"
                    extractor = ORB::create();
                    matcher = BFMatcher(NORM_HAMMING);
                    break;
                case 3: //"AKAZE"
                    extractor = AKAZE::create();
                    matcher = BFMatcher(NORM_HAMMING);
                    break;
                }
                try
                {
                    extractor->detectAndCompute(img1, Mat(), keypoints1, descriptors1);
                    extractor->detectAndCompute(imgn, Mat(), keypoints2, descriptors2);
                    matcher.match(descriptors1, descriptors2, matches);
                }
                catch (Exception *e)
                {
                    cout << " Keypoint extracting meets an ERROR! " << endl;
                    error_read++;
                    continue;
                }
                // 对特征点进行粗匹配
                double max_dist = 0;
                double min_dist = 100;
                for (int j = 0; j < matches.size(); j++)
                {
                    double dist = matches[j].distance;
                    if (dist < min_dist)
                        min_dist = dist;
                    if (dist > max_dist)
                        max_dist = dist;
                }
                for (int j = 0; j < matches.size(); j++)
                {
                    if (matches[j].distance <= max(2 * min_dist, 0.02))
                        good_matches.push_back(matches[j]);
                }
                if (good_matches.size() < 1)
                {
                    cout << " The number of valid keypoint is less then 1, rough match failed! " << endl;
                    error_read++;
                    continue;
                }
                // 计算粗匹配准确率
                // double accuracy = static_cast<double>(good_matches.size()) / static_cast<double>(keypoints1.size());
                // cout << "accuracy: " << accuracy << endl;

                // 使用RANSAC进行内点提纯
                vector<Point2f> points1, points2;
                for (const DMatch &match : good_matches)
                {
                    int queryIdx = match.queryIdx;
                    int trainIdx = match.trainIdx;

                    if (queryIdx >= 0 && queryIdx < keypoints1.size() &&
                        trainIdx >= 0 && trainIdx < keypoints2.size())
                    {
                        points1.push_back(keypoints1[queryIdx].pt);
                        points2.push_back(keypoints2[trainIdx].pt);
                    }
                }

                // 使用基础矩阵作为提纯模型
                Mat inliers_mask;
                Mat fundamental_matrix = findFundamentalMat(points1, points2, FM_RANSAC, 3, 0.99, inliers_mask);

                vector<DMatch> ransac_matches; // 提纯之后的内点
                int iii = 0;                   // 用于跟踪 inliers_mask 中的索引
                for (const DMatch &match : good_matches)
                {
                    if (iii < inliers_mask.rows && inliers_mask.at<uchar>(iii))
                    {
                        ransac_matches.push_back(match);
                    }
                    iii++;
                }

                innersize = ransac_matches.size();
                if (innersize == 0)
                {
                    error_read++;
                    // continue;  // 不要影响效率对比
                }

                // 计算准确率
                float ff = (float)innersize / (float)good_matches.size();
                // cout << "准确率/内点比例：" << ff << endl;
                ap += ff;

                // 如果效果较好，则保存。效果好指的是：特征点全部是内点（特征点包括内点和外点，内点能正确描述图像，外点是一些噪声点。）
                // Mat matTmp;
                // if (ff == 1.0) {
                //     drawMatches(img1, keypoints1, imgn, keypoints2, good_matches, matTmp);
                //     char charJ[255];
                //     sprintf_s(charJ, "_%d.jpg", i);
                //     string strResult = "D:/研究生课程/视频内容分析与实践/CODE/DETECTION/dataset/" + strDateset + "/" + strMethod + charJ;
                //     imwrite(strResult, matTmp);
                // }
                ff = 0;
                innersize = 0;
                matches.clear();
                good_matches.clear();
            }

            //  打印算法用时
            cout << "Average time of algorithm: " << ((getTickCount() - t) / getTickFrequency()) / 10 << "s/张" << endl;
            // 计算算法使用了多少张图像
            cout << "Number of used pictures: " << 10 - error_read << endl;
            // 平均准确率
            ap /= (10 - error_read);
            cout << "Average precision: " << ap << endl;

            // return 0;
        }
    }
    system("pause");
    return 0;
}

/********************可参考chatgpt给出的特征匹配样例**********************************/
/****************
#include <opencv2/opencv.hpp>
#include <opencv2/features2d.hpp>

int main() {
    cv::Mat image1 = cv::imread("image1.jpg", cv::IMREAD_GRAYSCALE);
    cv::Mat image2 = cv::imread("image2.jpg", cv::IMREAD_GRAYSCALE);

    cv::Ptr<cv::Feature2D> orb = cv::ORB::create();
    std::vector<cv::KeyPoint> keypoints1, keypoints2;
    cv::Mat descriptors1, descriptors2;
    orb->detectAndCompute(image1, cv::noArray(), keypoints1, descriptors1);
    orb->detectAndCompute(image2, cv::noArray(), keypoints2, descriptors2);

    cv::BFMatcher matcher(cv::NORM_HAMMING, true);
    std::vector<cv::DMatch> matches;
    matcher.match(descriptors1, descriptors2, matches);

    // 通过设置阈值筛选匹配项
    double max_dist = 0;
    double min_dist = 100;

    for (int i = 0; i < descriptors1.rows; i++) {
        double dist = matches[i].distance;
        if (dist < min_dist) min_dist = dist;
        if (dist > max_dist) max_dist = dist;
    }

    std::vector<cv::DMatch> good_matches;
    for (int i = 0; i < descriptors1.rows; i++) {
        if (matches[i].distance <= std::max(2 * min_dist, 30.0)) {
            good_matches.push_back(matches[i]);
        }
    }

    // 使用RANSAC进行内点提纯
    std::vector<cv::Point2f> points1, points2;
    for (const cv::DMatch& match : good_matches) {
        points1.push_back(keypoints1[match.queryIdx].pt);
        points2.push_back(keypoints2[match.trainIdx].pt);
    }

    cv::Mat inliers_mask;
    cv::Mat fundamental_matrix = cv::findFundamentalMat(points1, points2, cv::FM_RANSAC, 3, 0.99, inliers_mask);

    std::vector<cv::DMatch> ransac_matches;
    for (int i = 0; i < good_matches.size(); i++) {
        if (inliers_mask.at<uchar>(i)) {
            ransac_matches.push_back(good_matches[i]);
        }
    }

    // 计算RANSAC后的特征匹配准确率
    double ransac_accuracy = static_cast<double>(ransac_matches.size()) / static_cast<double>(keypoints1.size());

    std::cout << "RANSAC后的特征匹配准确率: " << ransac_accuracy << std::endl;

    return 0;
}
*************************/