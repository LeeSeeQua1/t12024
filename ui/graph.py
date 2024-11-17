from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QProgressBar, QHBoxLayout, QGridLayout

from sprint_health.sprint_health_api import get_spring_health


def get_bar_colour(percent: int):
    return '#083ef0'


fields = ["dvdev", "planed", "todo", "canceled", "backlog"]


class GraphWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self, sprint_id: int):
        super().__init__()
        self.lay = QGridLayout(self)
        self._values = get_spring_health(sprint_id - 1)
        self._slider = QSlider(Qt.Horizontal)
        self._slider.setMinimum(1)
        self._slider.setMaximum(len(self._values))
        self._slider.setTickInterval(1)
        self._slider.valueChanged.connect(self._on_update)
        self.lay.addWidget(self._slider, 0, 0, 1, len(fields))
        self._graphs = []
        self._display(self._values[0])

    def _on_update(self):
        frame = self._values[self._slider.value() - 1]
        self._display(frame)

    def _display(self, frame):
        for i in self._graphs:
            i.setParent(None)
        self._graphs.clear()
        for i, name in enumerate(fields):
            lay = QVBoxLayout()
            bar = QProgressBar()
            value = getattr(frame, name)
            bar.setValue(value * 100)
            bar.setOrientation(Qt.Vertical)
            bar.setFixedWidth(150)
            bar.setStyleSheet(f"""
                                QProgressBar {{
                border: 2px solid #8f8f91;
                border-radius: 5px;
                padding: 1px;
                background-color: #ffffff; /* White background for the bar */
                text-align: center; /* Text centered in the bar */
                color: #333; /* Dark text color */
            }}
            QProgressBar::chunk {{
                background-color: {get_bar_colour(value)}; /* Green for the filled portion */
                border-radius: 5px; /* Rounded corners for the filled portion */
            }}
                            """)
            lay.addWidget(bar)
            txt = QLabel(name)
            lay.addWidget(txt)
            self._graphs.append(lay)
            self._graphs.append(txt)
            self._graphs.append(bar)
            # self._progress_bars.append(bar)
            # self._progress_bars.append(txt)
            self.lay.addLayout(lay, 1, i)
