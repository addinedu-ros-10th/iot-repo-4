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

from_class = uic.loadUiType("graph.ui")[0]  # UI 파일 경로

class PieCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(2, 2))
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        self.draw_pie(0)

    def draw_pie(self, value):
        self.ax.clear()
        self.ax.set_aspect("equal", adjustable="box")

        val = [value, 1 - value]

        def make_autopct(values):
            def my_autopct(pct):
                total = sum(values)
                val = pct * total / 100.0
                return f"{val:.3f}"
            return my_autopct

        self.ax.pie(val,
                    colors=["skyblue", "lightgray"],
                    startangle=90,
                    autopct=make_autopct(val),
                    counterclock=False)
        self.draw()


class WindowClass(QMainWindow, from_class):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Multi Pie Graphs with Per-Sensor Normalization")

        # ✅ 센서별 정규화 범위 (소프트코딩)
        self.sensor_config = {
            "sensor1": {"min": 0, "max": 2},
            "sensor2": {"min": 0.5, "max": 2},
            "sensor3": {"min": 0, "max": 2},
            "sensor4": {"min": 0, "max": 2},
            "sensor5": {"min": 0.2, "max": 2}
        }

        # ✅ 센서 위젯 등록
        self.sensor_widgets = {
            "sensor1": self.widgetPlot_pie_1,
            "sensor2": self.widgetPlot_pie_2,
            "sensor3": self.widgetPlot_pie_3,
            "sensor4": self.widgetPlot_pie_4,
            "sensor5": self.widgetPlot_pie_5
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
            "sensor3": np.pi / 2,
            "sensor4": np.pi,
            "sensor5": np.pi * 2
        }

        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_pies)
        self.timer.start()

    def normalize(self, name, val):
        """센서별 정규화 처리"""
        config = self.sensor_config.get(name, {})
        min_v = config.get("min", 0)
        max_v = config.get("max", 1)

        if max_v == min_v:
            return 0.0
        return min(max((val - min_v) / (max_v - min_v), 0.0), 1.0)

    def update_pies(self):
        for name, canvas in self.sensor_canvases.items():
            phase_shift = self.phase[name]
            
            if phase_shift != "sensor3":
                y = np.sin(self.x[self.index] + phase_shift) + 1  # 0~2 사이의 값
            else:
                y = np.sin(self.x[self.index] + phase_shift) + 1  # 0~2 사이의 값
            y_norm = self.normalize(name, y)
            canvas.draw_pie(y_norm)

        self.index = (self.index + 1) % len(self.x)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    sys.exit(app.exec())
