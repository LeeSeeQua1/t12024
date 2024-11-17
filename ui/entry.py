from PySide6 import QtWidgets
from PySide6.QtCharts import QChart, QChartView, QBarCategoryAxis, QBarSeries, QBarSet, QValueAxis
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QTabWidget, QPushButton, QFileDialog, QVBoxLayout, QWidget, QHBoxLayout, \
    QLabel, QLineEdit, QGridLayout, QSlider, QProgressBar, QComboBox
import os

from sprint_health.sprint_health_api import get_spring_health, StateFrame

from database import data_split
from ui.graph import GraphWindow


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.l2 = QHBoxLayout(self)
        l1 = QVBoxLayout()
        self.l2.addLayout(l1)

        self._table_names = ["Sprints", "Tasks", "History"]
        btn1 = QPushButton(self._table_names[0])
        btn1.clicked.connect(lambda: self._choose_file(0))
        l1.addWidget(btn1)
        btn2 = QPushButton(self._table_names[1])
        btn2.clicked.connect(lambda: self._choose_file(1))
        l1.addWidget(btn2)
        btn3 = QPushButton(self._table_names[2])
        btn3.clicked.connect(lambda: self._choose_file(2))
        l1.addWidget(btn3)
        self._btns = [btn1, btn2, btn3]

        self._files: list[str | None] = [None, None, None]
        self._push_btn = QPushButton('Analyze')
        self._push_btn.clicked.connect(self._confirm)
        l1.addWidget(self._push_btn)
        self._graph_widget = None
        self.setGeometry(300, 150, 550, 300)

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
            path = dial.selectedFiles()[0]
            self._files[index] = path
            self._btns[index].setText(os.path.basename(path) + ' (' + self._table_names[index] + ')')

    def _confirm(self):
        if not all(self._files):
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.showMessage('You should attach all necessary tables')
            return

        if self.col_lay is not None:
            self.col_lay.setParent(None)

        # self._num_of_rows = data_split(*self._files)
        self._text = QLineEdit("1")
        self._combo = QComboBox()
        self._combo.setCurrentIndex(0)
        self._combo.currentIndexChanged.connect(self._get_combo_index)
        self._combo.addItems(data_split(*self._files))
        self.col_lay = QVBoxLayout()
        self.col_lay.addWidget(self._text)
        self._current_sprint_id = 0
        btn = QPushButton("push")
        btn.clicked.connect(lambda: self._get_sprint(self._current_sprint_id))
        self.col_lay.addWidget(btn)
        self.col_lay.addWidget(self._combo)
        self.l2.addLayout(self.col_lay)

    def _get_combo_index(self, sprint_id: int):
        print("here", sprint_id, type(sprint_id))
        self._current_sprint_id = sprint_id

    def _get_sprint(self, sprint_id: int):
        # try:
        #     sprint_id = int(sprint_id)
        # except ValueError:
        #     pass
        # if isinstance(sprint_id, str) or sprint_id > self._num_of_rows:
        #     error_dialog = QtWidgets.QMessageBox()
        #     error_dialog.setText('You should input number between 1 and number of sprints')
        #     error_dialog.exec()
        #     return
        self.window = GraphWindow(sprint_id)
        self.window.show()
