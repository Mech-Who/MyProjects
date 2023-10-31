# MotionCaptureSystem - Python

## 一、使用的技术

- python
- pyside6
- mediapipe
- opencv
- panda3d

## 二、软件结构

### 功能

1. 导入模型
    > 选择模型文件导入系统
    - 模型文件格式检测
    - 模型文件读取
    - 内容处理
    - 模型信息以json格式保存

2. 选择模型
    > 选择在预览效果中要使用的模型
    - 根据文件展示模型列表
      - 系统自带的模型
      - 用户已经导入的模型
    - 读取配置文件，选中默认模型（上一次选中的模型）
    - 根据鼠标点击，选中模型
      - 修改配置文件
      - 修改模型详情展示

3. 预览效果
    > 查看摄像头拍摄情况以及虚拟形象动作展示
    - 获取摄像头内容并展示
    - 摄像头内容经OpenCV处理
    - 处理后数据用于渲染虚拟形象

4. 直播展示
    > 做出直播的展示效果
    - live2d桌面显示（待定）
    - 软件框体内展示（待定）

5. 视频转换
    > 从文件导入视频，并将视频中的人替换为虚拟形象后输出
    - 选择视频文件作为输入
    - 播放视频文件
    - 渲染虚拟形象并与视频文件并列播放

## 三、界面设计

> 墨刀设计文档：https://modao.cc/app/ym8M4dBrsp08v5tjvga0Z 

1. 主界面
    - 模型列表
        - 模型详情展示和删除
        - 系统模型
        - 导入模型
        - 模型默认值展示与设置
        - 骨骼绑定界面
    - 效果预览
        - 预览开始与停止按钮
        - 摄像头画面
        - 渲染画面
    - 直播展示（待定）
        - live2d展示
        - live2d模型选择
    - 视频转换
        - 选择视频文件
        - 播放视频文件
        - 播放虚拟形象渲染结果
2. 导入模型界面
    - 选择模型文件
    - 选择模型格式
    - 模型图标展示
    - 导入结果提示

## 四、核心功能思路

1. Json文件控件
    通过TreeWidget控件，以递归的方式读取内容并写入Widget实现Json展示，然后通过itemChanged信号实现内容修改
    优化：
    1. 通过QTreeView来展示数据，似乎可以嵌入QSlider来调整数值，而不再是自己输入数值来进行调整
    2. 在模型默认值界面仅提供cameraPosition、cameraRotation和cameraTarget的展示和调整，其他的内容可以不显示
    3. 添加init的调整，按照骨骼对模型进行调整

2. OpenCV和Panda3d界面嵌入控件
    将OpenCV的图像帧或是Panda3d的渲染画面帧作为图像传到QLabel上，并按帧率更新即可实现嵌入。

    注意：
    1. 使用QTimer作为定时器，可以限制展示的帧率，同时可以通过控制定时器来控制内容播放的开关

3. 关键点驱动虚拟形象
    要点：
    1. 坐标从Mediapipe到Panda3d需要进行坐标轴转换(x, y, z)->(x, -z, y)
    2. 只需要控制四肢和头部的骨骼欧拉角旋转即可实现模型上的动作复现，无需对标关键点，即通过点对点的方式控制模型
    3. 展示模型时，应当根据模型大小，调整模型的位置、方向和缩放以及摄像头的位置、朝向
    4. 参考kalidokit实现，根据landmark2d和landmark3d得到骨骼的欧拉角

## 五、参考资料

- [qt官方文档](https://doc.qt.io/)
- [OpenCV教学视频](https://www.bilibili.com/video/BV1Fo4y1d7JL)
- [OpenCV官方文档](https://docs.opencv.org/4.7.0/)
- [MediaPipe官方文档](https://developers.google.com/mediapipe/framework/getting_started/install.md#installing_on_windows)

## 六、问题记录

1. Error: File 'ui_importmodel.ui' is not valid
    > 问题描述：在运行程序时，报错：Error: File 'ui_importmodel.ui' is not valid
    >  
    > 问题原因：配置external tools时，工作目录要确定好，否则会出现找不到文件的情况，导致无法运行。如：配置uic的工作目录为项目的目录，但是由于我把*.ui后来都放到gen目录下了，导致uic找不到文件，无法运行。
    >
    > 解决方案：配置工作目录为$ProjectFileDir$\gen
