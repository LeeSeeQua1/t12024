import os

from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog, QPushButton, QHBoxLayout, QVBoxLayout


class FileSelectionDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Files")
        self.setGeometry(400, 200, 400, 200)

        # Layout
        layout = QVBoxLayout(self)

        self._table_names = ["Sprints", "Tasks", "History"]
        self._btns = []
        self._files = [None, None, None]

        # Buttons for each file
        for i, name in enumerate(self._table_names):
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, idx=i: self._choose_file(idx))
            layout.addWidget(btn)
            self._btns.append(btn)

        # Proceed and Abort Buttons
        btn_layout = QHBoxLayout()
        proceed_btn = QPushButton("Proceed")
        proceed_btn.clicked.connect(self._proceed)
        btn_layout.addWidget(proceed_btn)

        abort_btn = QPushButton("Abort")
        abort_btn.clicked.connect(self.reject)  # Close the dialog without saving
        btn_layout.addWidget(abort_btn)

        layout.addLayout(btn_layout)

    def _choose_file(self, index: int):
        dial = QFileDialog(self)
        dial.setNameFilter("Csv (*.csv)")
        if dial.exec():
            path = dial.selectedFiles()[0]
            self._files[index] = path
            self._btns[index].setText(os.path.basename(path) + ' (' + self._table_names[index] + ')')

    def _proceed(self):
        if not all(self._files):
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.showMessage('You should attach all necessary tables')
            return
        self.accept()  # Close dialog and save files

    def get_files(self):
        return self._files



