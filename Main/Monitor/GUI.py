import sys
import sqlite3 as sql
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QGridLayout, QWidget, QPushButton, QLineEdit, QLabel, QSpacerItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from datetime import datetime
import pandas as pd
from DBFunc import DBInit, DBClose
from DBVisual import getWindow

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure()
        super().__init__(fig)
        self.ax = fig.add_subplot(111)
        self.fig = fig

    def plot(self, data:pd.DataFrame, title:str):
        x = data["DATETIME"]
        y = data.loc[:, ~data.columns.isin(["DATETIME", "HOUSE"])]

        self.ax.clear()
        self.ax.plot(x,y, linewidth=2)
        self.ax.set_xlabel("Date/Time")
        self.ax.set_ylabel("Signal Measurements")
        self.ax.set_title(title)
        self.ax.xaxis.set_major_locator(MaxNLocator(nbins=10))
        self.ax.set_xticklabels(x, rotation=30, ha= 'right')
        self.ax.legend(y.columns)

        self.fig.tight_layout()
        self.draw()


class App(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("View Greenhouse Signals")
        self.setGeometry(100,100,800,800)
        self.canvas = PlotCanvas(self)
        self.canvas.setSizeIncrement(0,100)
        self.draw_button = QPushButton("View TimeFrame")
        self.draw_button.clicked.connect(self.viewData)
        self.houseLabel  = QLabel("HouseSelect")
        self.houseSelect = QLineEdit("1")
        self.StartLabel  = QLabel("Start Date")
        self.dtStart     = QLineEdit(f"{datetime.today().year}-{datetime.today().month}")
        self.EndLabel    = QLabel("End Date")
        self.dtEnd       = QLineEdit(datetime.today().date().__str__())

        layout = QVBoxLayout()
        grid = QGridLayout()
        grid.setSpacing(5)

        
        grid.addWidget(self.houseLabel,  1, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.houseSelect, 1, 1)
        grid.addWidget(self.StartLabel,  2, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.dtStart,     2, 1)
        grid.addWidget(self.EndLabel,    3, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.dtEnd,       3, 1)

        layout.addLayout(grid)
        layout.addWidget(self.draw_button)
        layout.addWidget(self.canvas)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def viewData(self)->None:
        path = "Main\\Monitor\\test.db"

        con,error = DBInit(path)

        if not con:
            return
        
        df: pd.DataFrame = getWindow(con,self.dtStart.text(), self.dtEnd.text(), (int)(self.houseSelect.text()))
        con.close()

        self.canvas.plot(df, f"House: {self.houseSelect.text()} Date/Time: {self.dtStart.text()} -- {self.dtEnd.text()}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
        