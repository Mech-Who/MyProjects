# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication
from MotionCaptureSystem import MotionCaptureSystem

# 程序入口
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MotionCaptureSystem()
    window.show()

    sys.exit(app.exec())
