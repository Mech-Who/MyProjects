# OpenCVPractice 说明

## 外部工具使用

> 记得要进入到OpenCVPractice目录再执行以下命令，否则会失败哦！

- designer：

  作用：设计界面

  工具路径：`C:\UserData\Environment\Tools\anaconda_data\envs\projects\Library\bin\designer.exe`

  命令使用格式：

- uic

  作用：将根据 ui 文件生成 UI 的 py 文件

  工具路径：

  - `C:\UserData\Environment\Tools\anaconda_data\envs\projects\Scripts\pyside6-uic.exe`
  - `C:\UserData\Environment\Tools\anaconda_data\envs\projects\Library\bin\uic.exe`

  命令使用格式：

  - `pyside6-uic ./ui/<源文件名>.ui -o ./ui/ui_<输出文件名>.py`
  - `uic -g python -o ./ui/ui_<输出文件名>.py ./ui/<源文件名>.ui`

- rcc

  作用：生成包含所有资源二进制信息的 Python 类，参考：`https://blog.csdn.net/baidu_36499789/article/details/119490603`

  工具路径：

  - `C:\UserData\Environment\Tools\anaconda_data\envs\projects\Scripts\pyside6-rcc.exe`
  - `C:\UserData\Environment\Tools\anaconda_data\envs\projects\Library\bin\rcc.exe`

  命令使用格式：

  - `pyside6-rcc ./rc/<资源文件名>.qrc -o ./rc/rc_<资源文件名>.py`
  - `rcc -g python -o ./rc/rc_<资源文件名>.py ./rc/<资源文件名>.qrc`

    注意：在运行命令之前，要先把资源添加到 .qrc 文件中。下面的例子展示了 icons.qrc 文件中列出的资源。

    ```qrc
    </ui>
    <!DOCTYPE RCC><RCC version="1.0">
    <qresource>
        <file>icons/play.png</file>
        <file>icons/pause.png</file>
        <file>icons/stop.png</file>
        <file>icons/previous.png</file>
        <file>icons/forward.png</file>
    </qresource>
    </RCC>
    ```

- auto-py-to-exe

  作用：基于 pyinstaller 的带 Ui 界面的打包程序，对新手极其友好。

  命令使用格式：auto-py-to-exe
