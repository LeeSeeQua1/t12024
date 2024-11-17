from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QComboBox, QLabel

from database import data_split
from ui.graph import GraphWindow
from ui.select_dialog import FileSelectionDialog


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self._lay = QVBoxLayout(self)

        self._header_label = QLabel("Welcome to Sprint Data Analyzer")
        self._header_label.setStyleSheet("font-size: 18px; font-weight: bold; text-align: center;")
        self._header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._lay.addWidget(self._header_label)

        description_label = QLabel(
            "Select your CSV files to analyze sprint data.\n"
            "Once files are selected, choose a sprint to proceed."
        )
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setStyleSheet("color: gray; font-size: 14px;")
        self._lay.addWidget(description_label)

        self._confirm_btn = None
        self._combo = None
        self._files: list[str | None] = [None, None, None]
        self._push_btn = QPushButton('Analyze')
        self._push_btn.clicked.connect(self._confirm)
        self._graph_widget = None
        self.setGeometry(300, 150, 550, 300)

        self._file_select_btn = QPushButton("Select Files")
        self._file_select_btn.clicked.connect(self._open_file_dialog)
        self._lay.addWidget(self._file_select_btn)
        self._file_select_btn.setStyleSheet("padding: 8px 16px; font-size: 14px;")

    def _open_file_dialog(self):
        dialog = FileSelectionDialog(self)
        if dialog.exec():
            self._files = dialog.get_files()
            self._confirm()
            self._header_label.setText("Press again to choose another file")

    def _confirm(self):
        if not all(self._files):
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.showMessage('You should attach all necessary tables')
            return

        self._current_sprint_id = 0
        if self._combo is None:
            self._combo = QComboBox()
            self._combo.setCurrentIndex(0)
            self._combo.currentIndexChanged.connect(self._get_combo_index)
            self._combo.addItems(data_split(*self._files))
            self._lay.addWidget(self._combo)
        else:
            self._combo.setCurrentIndex(0)
            self._combo.clear()
            self._combo.currentIndexChanged.connect(self._get_combo_index)
            self._combo.addItems(data_split(*self._files))
        if self._confirm_btn is None:
            self._confirm_btn = QPushButton("Confirm sprint selection")
            self._confirm_btn.setStyleSheet("padding: 8px 16px; font-size: 14px;")
            self._confirm_btn.clicked.connect(lambda: self._get_sprint(self._current_sprint_id))
            self._lay.addWidget(self._confirm_btn)

    def _get_combo_index(self, sprint_id: int):
        self._current_sprint_id = sprint_id

    def _get_sprint(self, sprint_id: int):
        self.window = GraphWindow(sprint_id)
        self.window.show()
