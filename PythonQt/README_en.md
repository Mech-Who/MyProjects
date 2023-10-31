# MotionCaptureSystem - Python

## 1. Used Technology

- python
- pyside6
- mediapipe
- opencv

## 2. Software Structure

### Functions
1. Import Model
    > Select model file and import to the system.

    - File format detection
    - Read model file
    - Process the model content
    - Save the model

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

## 界面设计
> 墨刀设计文档：https://modao.cc/app/ym8M4dBrsp08v5tjvga0Z 

1. 主界面
   - 模型列表
     - 模型详情展示
     - 系统模型
     - 导入模型
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

## 参考资料
- [qt official document](https://doc.qt.io/)
- [OpenCV tutorial](https://www.bilibili.com/video/BV1Fo4y1d7JL)
- [OpenCV official document](https://docs.opencv.org/4.7.0/)
- [MediaPipe official document](https://developers.google.com/mediapipe/framework/getting_started/install.md#installing_on_windows)