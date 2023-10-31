# This Python file uses the following encoding: utf-8
import sys
import random
from PySide6 import QtWidgets, QtCore, QtQml

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World", alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))


QML = """
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Window {
    width: 300
    height: 200
    visible: true
    title: "Hello World"

    readonly property list<string> texts: ["Hallo Welt", "Hei maailma",
                                           "Hola Mundo", "Привет мир"]

    function setText() {
        var i = Math.round(Math.random() * 3)
        text.text = texts[i]
    }

    ColumnLayout {
        anchors.fill:  parent

        Text {
            id: text
            text: "Hello World"
            Layout.alignment: Qt.AlignHCenter
        }
        Button {
            text: "Click me"
            Layout.alignment: Qt.AlignHCenter
            onClicked:  setText()
        }
    }
}
"""

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # new mainwindow
    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    # qt quick
    engine = QtQml.QQmlApplicationEngine()
    engine.loadData(QML.encode('utf-8'))
    if not engine.rootObjects():
        sys.exit(-1)
    exit_code = app.exec()
    del engine

    sys.exit(app.exec())
