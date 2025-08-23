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

        self.x = np.linspace(0, 200, 2000)
        self.gas = np.linspace(0, 100, len(self.x))
        self.temperature = 20 + 10 * self.x
        self.weight_rice = 50 + 30 * np.sin(self.x / 40)
        self.weight_bed = 100 + 20 * np.cos(self.x / 60)
        self.weight_laundry = 70 + 10 * np.sin(self.x / 20)

        # ✅ 센서별 정규화 범위 (소프트코딩)
        self.sensor_config = {
            "sensor1": {"min": 0, "max": 100},
            "sensor2": {"min": 0.5, "max": 200},
            "sensor3": {"min": 0, "max": 200},
            "sensor4": {"min": 0, "max": 300},
            "sensor5": {"min": 0.2, "max": 300}
        }

        # ✅ 센서 위젯 등록
        self.sensor_widgets = {
            "sensor1": self.widgetPlot_pie_1,
            "sensor2": self.widgetPlot_pie_2,
            "sensor3": self.widgetPlot_pie_3,
            "sensor4": self.widgetPlot_pie_4,
            "sensor5": self.widgetPlot_pie_5
        }

        self.sensor_values = {
            "sensor1": self.gas,           # 가스 센서
            "sensor2": self.temperature,   # 온도
            "sensor3": self.weight_rice,   # 쌀 무게
            "sensor4": self.weight_bed,    # 침대 무게
            "sensor5": self.weight_laundry # 세탁물 무게
        }

        self.sensor_canvases = {}
        for name, widget in self.sensor_widgets.items():
            canvas = PieCanvas(widget)
            layout = QVBoxLayout(widget)
            layout.addWidget(canvas)
            self.sensor_canvases[name] = canvas

        # 테스트용 사인 곡선 (센서별 phase 다르게)
        self.index = 0

        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_pies)
        self.timer.start()

        self.decide_crisis_level()
        self.show_crisis_contents()

    def decide_crisis_level(self):
        self.label_crlevel.setText("qqq")
        return

    def show_crisis_contents(self):
        self.line_crcontents.setText("qqq")
        return

    def normalize(self, name, val):
        """센서별 정규화 처리"""
        config = self.sensor_config.get(name, {})
        min_v = config.get("min", 0)
        max_v = config.get("max", 1)

        if max_v == min_v:
            return 0.0
        return min(max((val - min_v) / (max_v - min_v), 0.0), 2.0)

    def update_pies(self):
        for name, canvas in self.sensor_canvases.items():
            data = self.sensor_values.get(name)
            if data is not None and self.index < len(data):
                value = data[self.index]
                norm = self.normalize(name, value)
                canvas.draw_pie(norm)

        self.index += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    sys.exit(app.exec())