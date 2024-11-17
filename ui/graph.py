from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QGridLayout, QHBoxLayout
from PySide6.QtGui import QColor

from sprint_health.sprint_health_api import get_spring_health
from ui.models import CustomProgressBar


def get_bar_colour(percent: int, first: int = 100, second: int = 0):
    if percent < first:
        return "#00ff00"
    if percent < second:
        return "#ffa500"
    return "#ff0000"


red = QColor(190, 30, 30)
orange = QColor(250, 100, 10)
green = QColor(0, 150, 0)


# fields = [("dvdev", {70: orange, 90: red}), ("planed", {}), ("todo", {20: red}), ("canceled", {10: red}),
#           ("backlog", {50: red, 20: orange})]


class GraphWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self, sprint_id: int, d):
        super().__init__()
        self._graph_width = 150
        self.lay = QGridLayout(self)
        self.lay.setSpacing(30)
        self._d = d
        pad = 30
        self.lay.setContentsMargins(pad, pad, pad, pad)
        self._values = get_spring_health(sprint_id)
        self._slider = QSlider(Qt.Horizontal)
        self._slider.setMinimum(1)
        self._slider.setMaximum(len(self._values))
        self._slider.setTickInterval(1)
        self._slider.valueChanged.connect(self._on_update)

        self._slider_value_label = QLabel(f"Date: {self._get_current_frame_date()}")
        self._slider_value_label.setAlignment(Qt.AlignCenter)

        self.lay.addWidget(self._slider, 1, 0, 1, len(self._d))
        self.lay.addWidget(self._slider_value_label, 0, 0, 1, len(self._d))
        self._graphs = []
        self._display(self._values[0])
        self.setGeometry(self._graph_width, self._graph_width, self._graph_width * len(self._d) + 100, 480)

        label = QLabel("""
1) Ошибки - указывает, на то какое количество времени было потрачено на ошибки.
2) По плану - процент задач, которые завершены в выбранный день.
3) В работе - процент задач, которые находятся в разработке в данный момент.
4) Снято - процент отмененных задач.
5) Оценка изменения бэклога - показывает на сколько верно было изначально оценены задачи.
 Точное значение: отношение оценок задач добавленных после начала спринта к оценкам начальных задач.
""")
        self.lay.addWidget(label, 4, 0, 1, 5)

    def _on_update(self):
        frame = self._values[self._slider.value() - 1]
        self._slider_value_label.setText(f"Date: {self._get_current_frame_date()}")
        self._display(frame)

    def _get_current_frame_date(self):
        return self._values[self._slider.value() - 1].Data.strftime("%d.%m.%y")

    def _display(self, frame):
        for i in self._graphs:
            i.setParent(None)
        self._graphs.clear()
        for i, (name, lines) in enumerate(self._d):
            lay = QVBoxLayout()
            lay.setAlignment(Qt.AlignCenter)
            bar = CustomProgressBar(lines)
            value = getattr(frame, name)
            bar.setValue(value * 100)
            bar.setTextVisible(False)
            bar.setOrientation(Qt.Vertical)
            bar.setFixedWidth(self._graph_width)
            bar.setStyleSheet(f"""
                                QProgressBar {{
                border: 2px solid #8f8f91;
                border-radius: 5px;
                padding: 1px;
                background-color: #ffffff;
                color: #333;
            }}
            QProgressBar::chunk {{
                background-color: {get_bar_colour(value * 100, *lines.keys())}; 
                border-radius: 5px; 
            }}
                            """)
            txt_ = QLabel(f"          {value * 100:.2f}%")
            txt_.setStyleSheet("font-size: 14px; font-weight: bold;")
            lay.addWidget(txt_)
            lay.addWidget(bar)
            txt = QLabel('\t ' + name)
            txt.setStyleSheet("font-size: 14px; font-weight: bold;")
            lay.addWidget(txt)
            self._graphs.append(lay)
            self._graphs.append(txt)
            self._graphs.append(txt_)
            self._graphs.append(bar)
            self.lay.addLayout(lay, 2, i)
