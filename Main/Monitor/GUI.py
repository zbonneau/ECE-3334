import sys
import sqlite3 as sql
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QGridLayout, QWidget, QPushButton, QLineEdit, QLabel, QTabWidget
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
        for label in self.ax.get_xticklabels():
            label.set_rotation(30)
            label.set_ha('right')
        self.ax.legend(y.columns)

        self.fig.tight_layout()
        self.draw()

class DataViewTab(QWidget):
    def __init__(self) -> None:
        super().__init__()
        # self.tabLabel = QLabel("View GreenHouse Data")
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

        # layout.addWidget(self.tabLabel)
        layout.addLayout(grid)
        layout.addWidget(self.draw_button)
        layout.addWidget(self.canvas)

        self.setLayout(layout)
        

    def viewData(self)->None:
        path = "Main\\Monitor\\test.db"

        con,error = DBInit(path)

        if not con:
            return
        
        df: pd.DataFrame = getWindow(con,self.dtStart.text(), self.dtEnd.text(), (int)(self.houseSelect.text()))
        con.close()

        self.canvas.plot(df, f"House: {self.houseSelect.text()} Date/Time: {self.dtStart.text()} -- {self.dtEnd.text()}")

class HouseConfigTab(QWidget):
    def __init__(self)->None:
        super().__init__()
        # self.tabLabel = QLabel("Configure House Parameters")
        self.getCurrent = QPushButton("Get Current Parameters")
        self.getCurrent.clicked.connect(self.getCurrentParams)
        self.setNew  = QPushButton("Set House Parameters")
        self.setNew.clicked.connect(self.setParams)
        self.houseLabel = QLabel("Select House")
        self.houseValue = QLineEdit("1")

        self.tempMinLabel = QLabel("Temp Min")
        self.tempMinValue = QLineEdit()
        self.tempMaxLabel = QLabel("Temp Max")
        self.tempMaxValue = QLineEdit()
        
        self.HumdMinLabel = QLabel("Humidity Min")
        self.HumdMinValue = QLineEdit()
        self.HumdMaxLabel = QLabel("Humidity Max")
        self.HumdMaxValue = QLineEdit()
        
        self.MoistMinLabel = QLabel("Soil Moisture Min")
        self.MoistMinValue = QLineEdit()
        self.MoistMaxLabel = QLabel("Soil Moisture Max")
        self.MoistMaxValue = QLineEdit()

        self.configureLabel =  QLabel("Config Results: ")
        self.configureResult = QLabel("")

        layout = QVBoxLayout()
        grid = QGridLayout()
        grid.setSpacing(5)
        grid.addWidget(self.houseLabel, 0,0, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.houseValue, 0, 1)
        grid.addWidget(self.tempMinLabel, 1, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.tempMinValue, 1, 1)
        grid.addWidget(self.tempMaxLabel, 1, 2, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.tempMaxValue, 1, 3)
        grid.addWidget(self.HumdMinLabel, 2, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.HumdMinValue, 2, 1)
        grid.addWidget(self.HumdMaxLabel, 2, 2, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.HumdMaxValue, 2, 3)
        grid.addWidget(self.MoistMinLabel, 3, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.MoistMinValue, 3, 1)
        grid.addWidget(self.MoistMaxLabel, 3, 2, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.MoistMaxValue, 3, 3)
        grid.addWidget(self.setNew, 4,0, 1, 4)
        grid.addWidget(self.configureLabel, 5, 0, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.configureResult, 5, 1, 1, 3, alignment = Qt.AlignmentFlag.AlignTop)

        # layout.addWidget(self.tabLabel)
        layout.addWidget(self.getCurrent)
        layout.addLayout(grid)
        # layout.addWidget(self.setNew)
        # layout.addWidget(self.configureResult)

        self.setLayout(layout)
        
        

    def getCurrentParams(self)->None:
        pass

    def setParams(self)->None:
        pass


class App(QMainWindow):
    def __init__(self)->None:
        super().__init__()
        self.setWindowTitle("Automated Greenhouse")
        self.setGeometry(100,100,800,800)

        container = QTabWidget()
        container.addTab(DataViewTab(), "View Data")
        container.addTab(HouseConfigTab(), "Config House")
        self.setCentralWidget(container)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
        