from PySide6 import QtWidgets
from PySide6.QtWidgets import QMainWindow, QTabWidget, QPushButton, QFileDialog, QVBoxLayout, QWidget, QHBoxLayout, \
    QLabel, QLineEdit

from sprint_health.sprint_health_api import get_spring_health


# from database import data_split


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
        self.setLayout(self.l2)
        self._graph_widget = None

    def _choose_file(self, index: int):
        dial = QFileDialog(self)
        dial.setNameFilter("Csv (*.csv)")
        if dial.exec():
            path = dial.selectedFiles()
            self._files[index] = path

    def _confirm(self):
        # if not all(self._files):
        #     error_dialog = QtWidgets.QErrorMessage()
        #     error_dialog.showMessage('You should clip all necessary tables')
        #     return
        # self.l2.addWidget(Graph(data_split(*self._files)))

        if self._graph_widget is not None:
            self._graph_widget.setParent(None)

        self._graph_widget = Graph(10)
        self.l2.addWidget(self._graph_widget)


class Graph(QWidget):
    def __init__(self, num_of_rows: int):
        super().__init__()
        self._num_of_rows = num_of_rows
        self._text = QLineEdit("Text")
        layout = QVBoxLayout()
        layout.addWidget(self._text)
        self.setLayout(layout)
        btn = QPushButton("push")
        btn.clicked.connect(lambda: self._get_sprint(self._text.text()))
        layout.addWidget(btn)

    def _get_sprint(self, sprint_id: str):

        try:
            sprint_id = int(sprint_id)
        except ValueError:
            pass
        if isinstance(sprint_id, str) or sprint_id > self._num_of_rows:
            error_dialog = QtWidgets.QMessageBox()
            error_dialog.setText('You should clip all necessary tables')
            error_dialog.exec()
            return
        ls = get_spring_health(sprint_id)
        for i in ls:
            print(i)
