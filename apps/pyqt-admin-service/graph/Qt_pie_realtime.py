import sys
import numpy as np
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QTimer
from PyQt6 import uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import warnings
warnings.filterwarnings("ignore", category=UserWarning, 
                        message=".*Ignoring fixed x limits.*")

from_class = uic.loadUiType("graph.ui")[0]  # UI 파일 이름에 맞게 변경

class PieCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(2, 2))
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        self.draw_pie(0)  # 초기 상태

    def draw_pie(self, value):
        self.ax.clear()
        self.ax.set_aspect("equal", adjustable="box")

        # 파이그래프 비율 계산 (0~1 값)
        filled = value
        remaining = 1 - filled
        val = [remaining, filled]
        def make_autopct(values):
            def my_autopct(pct):
                total = sum(values)
                val = pct*total/100.0
                return f"{val:.3f}"  # or f"{val}개" 등으로 표시 가능
            return my_autopct

        self.ax.pie(val,
                    colors=["skyblue", "lightgray"],
                    startangle=90, autopct=make_autopct(val),
                    counterclock=False)
        self.draw()



class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Multi Pie Graphs!")

        # 센서 파이그래프를 담을 딕셔너리
        self.sensor_widgets = {
            "sensor1": self.widgetPlot_pie_1,
            "sensor2": self.widgetPlot_pie_2,
            "sensor3": self.widgetPlot_pie_3,
            # 필요에 따라 추가
        }

        self.sensor_canvases = {}
        for name, widget in self.sensor_widgets.items():
            canvas = PieCanvas(widget)
            layout = QVBoxLayout(widget)
            layout.addWidget(canvas)
            self.sensor_canvases[name] = canvas

        # 테스트용 사인 곡선 (센서별 phase 다르게)
        self.index = 0
        self.x = np.linspace(0, 2 * np.pi, 200)
        self.phase = {
            "sensor1": 0,
            "sensor2": np.pi / 3,
            "sensor3": np.pi / 2
        }

        # 타이머로 업데이트
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_pies)
        self.timer.start()

    def update_pies(self):
        for name, canvas in self.sensor_canvases.items():
            phase_shift = self.phase[name]
            y = (np.sin(self.x[self.index] + phase_shift) + 1) / 2  # 정규화
            canvas.draw_pie(y)

        self.index = (self.index + 1) % len(self.x)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    sys.exit(app.exec())
