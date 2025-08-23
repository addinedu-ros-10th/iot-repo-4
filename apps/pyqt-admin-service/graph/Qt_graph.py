import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6 import uic
import pyqtgraph as pg
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from_class = uic.loadUiType("graph.ui")[0]

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("Graph!")

        # self.plot = pg.PlotWidget(self.widgetPlot)   # widgetPlot 자리에 붙임
        # self.plot.plot([0,1,2,3,4], [10,3,8,2,7], pen='y')

        self.create_layout(1, 13, 4)
        self.create_layout(2, 4, 3)
        self.create_layout(3, 5, 3)
        self.create_layout(4, 6, 2)


    def create_layout(self, i, a, b):
        order = getattr(self, f"widgetPlot_pie_{i}")
        
        layout = QVBoxLayout(order)
        self.fig = Figure(figsize=(3,3))
        self.fig.tight_layout()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)


        self.draw_pie(a, b)


    def draw_pie(self, a, b):
        sizes = [a, b]
        labels = ["G", "R"]

        
        ax = self.fig.add_subplot(111)
        
        ax.clear()  # 새로 그릴 때는 지우기

        def make_autopct(values):
            def my_autopct(pct):
                total = sum(values)
                val = int(round(pct*total/100.0))
                return f"{val}"  # or f"{val}개" 등으로 표시 가능
            return my_autopct
        ax.pie(sizes, labels=labels, autopct=make_autopct(sizes), startangle=90, labeldistance=1.2, pctdistance=0.7)
        ax.axis("equal")  # 원형 유지
        
        self.fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        self.canvas.draw()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()

    sys.exit(app.exec())
