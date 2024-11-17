from PySide6 import QtWidgets
from PySide6.QtCharts import QChart, QChartView, QBarCategoryAxis, QBarSeries, QBarSet, QValueAxis
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QTabWidget, QPushButton, QFileDialog, QVBoxLayout, QWidget, QHBoxLayout, \
    QLabel, QLineEdit, QGridLayout, QSlider, QProgressBar

from sprint_health.sprint_health_api import get_spring_health, StateFrame

from database import data_split


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.l2 = QHBoxLayout(self)
        l1 = QVBoxLayout()
        self.l2.addLayout(l1)

        tmp = ["Sprints", "Tasks", "History"]
        btn = QPushButton(tmp[0])
        btn.clicked.connect(lambda: self._choose_file(0))
        l1.addWidget(btn)
        btn = QPushButton(tmp[1])
        btn.clicked.connect(lambda: self._choose_file(1))
        l1.addWidget(btn)
        btn = QPushButton(tmp[2])
        btn.clicked.connect(lambda: self._choose_file(2))
        l1.addWidget(btn)

        self._files: list[str | None] = [None, None, None]
        self._push_btn = QPushButton('Analyze')
        self._push_btn.clicked.connect(self._confirm)
        l1.addWidget(self._push_btn)
        self._graph_widget = None
        self.setGeometry(300, 150, 350, 300)

#
        self.col_lay = None
        self._num_of_rows = None
        self._text = None
        self._slider = None
        self._values: list[StateFrame] = []
        self._progress_bars = []

    def _choose_file(self, index: int):
        dial = QFileDialog(self)
        dial.setNameFilter("Csv (*.csv)")
        if dial.exec():
            path = dial.selectedFiles()
            self._files[index] = path[0]

    def _confirm(self):
        # if not all(self._files):
        #     error_dialog = QtWidgets.QErrorMessage()
        #     error_dialog.showMessage('You should clip all necessary tables')
        #     return
        # self.l2.addWidget(Graph(data_split(*self._files)))

        if self.col_lay is not None:
            self.col_lay.setParent(None)
            # self._graph_widget.setParent(None)

        # print(self._files, "data_split call")
        # self._graph_widget = Graph(data_split(*self._files))
        # self._graph_widget = Graph(10, self.l2)
        self._num_of_rows = data_split(*self._files)
        self._text = QLineEdit("1")
        self.col_lay = QVBoxLayout()
        self.col_lay.addWidget(self._text)
        btn = QPushButton("push")
        btn.clicked.connect(lambda: (print(self._text.text()), self._get_sprint(self._text.text())))
        self.col_lay.addWidget(btn)
        self.l2.addLayout(self.col_lay)

    def _get_sprint(self, sprint_id: str):
        try:
            sprint_id = int(sprint_id)
        except ValueError:
            pass
        if isinstance(sprint_id, str) or sprint_id > self._num_of_rows:
            error_dialog = QtWidgets.QMessageBox()
            error_dialog.setText('You should input number between 1 and number of sprints')
            error_dialog.exec()
            return
        if self._slider is not None:
            self._slider.setParent(None)
        self._values = get_spring_health(sprint_id)
        self._slider = QSlider(Qt.Horizontal)
        self._slider.setMinimum(1)
        self._slider.setMaximum(len(self._values))
        self._slider.setTickInterval(1)
        self._slider.valueChanged.connect(self._on_update)
        self.col_lay.addWidget(self._slider)

    def _on_update(self):
        if self._progress_bars:
            for i in self._progress_bars:
                i.setParent(None)
            self._progress_bars.clear()
        frame = self._values[self._slider.value()]
        self._progress_bars = []
        ls = ["dvdev", "planed", "todo", "canceled", "backlog"]
        for name in ls:
            lay = QVBoxLayout()
            bar = QProgressBar()
            bar.setValue(getattr(frame, name) * 100)
            bar.setOrientation(Qt.Vertical)
            bar.setFixedWidth(150)
            bar.setStyleSheet("""
                        QProgressBar {
        border: 2px solid #8f8f91;
        border-radius: 5px;
        padding: 1px;
        background-color: #ffffff; /* White background for the bar */
        text-align: center; /* Text centered in the bar */
        color: #333; /* Dark text color */
    }
    QProgressBar::chunk {
        background-color: #4CAF50; /* Green for the filled portion */
        border-radius: 5px; /* Rounded corners for the filled portion */
    }
                    """)
            lay.addWidget(bar)
            txt = QLabel(name)
            lay.addWidget(txt)
            self._progress_bars.append(lay)
            # self._progress_bars.append(bar)
            # self._progress_bars.append(txt)
            self.l2.addLayout(lay)

        # for i in self._progress_bars:
        #     self.l2.addLayout(i)
        print(frame.Data)

    def _get_bar_color(self, index: int):
        colors = ["#4CAF50", "#2196F3", "#FFC107", "#F44336", "#9C27B0"]
        return colors[index % len(colors)]


class Graph(QWidget):
    def __init__(self, num_of_rows: int, layout):
        super().__init__()
