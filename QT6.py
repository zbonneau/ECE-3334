import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

class firstWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hello World","Hei maailma", "Hola Mundo"]

        self.button = QtWidgets.QPushButton("Click Me")
        self.text   = QtWidgets.QLabel("Hello World", alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = firstWidget()
    widget.resize(800,600)
    widget.show()

    sys.exit(app.exec())

    