from PySide6.QtWidgets import QMainWindow
from ui.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    ui = Ui_MainWindow()
    def __init__(self):
        super().__init__()
        self.ui.setupUi(self)
