from copy import deepcopy

from PySide6.QtGui import QColor, QAction
from PySide6.QtWidgets import QMainWindow, QTabWidget, QHBoxLayout, QPushButton, QLineEdit, QVBoxLayout, QFormLayout, \
    QDialog

from ui.entry import Window

red = QColor(190, 30, 30)
orange = QColor(250, 100, 10)
green = QColor(0, 150, 0)

ls = [("dvdev", {10: orange, 15: red}), ("planed", {}), ("todo", {20: red}), ("canceled", {10: red}),
      ("backlog", {50: red, 20: orange})]


class EditDialog(QDialog):
    def __init__(self, key_name, data: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Edit Values for {key_name}")
        self.setGeometry(400, 200, 400, 300)

        self.key_name = key_name
        self.data = data
        self.updated_data = deepcopy(data)
        main_layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        self.inputs = {}
        for key, value in data.items():
            line_edit = QLineEdit(str(key))
            form_layout.addRow(f"Threshold {value.name()}:", line_edit)
            self.inputs[line_edit] = key  # Store mapping of QLineEdit to original key

        main_layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self._save)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        main_layout.addLayout(button_layout)

    def _save(self):
        """Update the data dictionary with the values from the dialog."""
        self.updated_data.clear()
        for input_field, original_key in self.inputs.items():
            try:
                new_key = int(input_field.text())  # Convert input to integer
                self.updated_data[new_key] = self.data[original_key]
                self.data.pop(original_key)
            except ValueError:
                continue
        self.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu('Файл')
        self._d = deepcopy(ls)
        for i in ls:
            if len(i[1]) == 0:
                continue
            action = QAction(f'Change {i[0]}', self)
            action.triggered.connect(lambda checked, name=i[0]: self._action(name))
            self.file_menu.addAction(action)
        self._window = Window(self._d)
        self.setCentralWidget(self._window)
        self.setGeometry(300, 150, 550, 300)

    def _action(self, key_name: str):
        for item in self._d:
            if item[0] == key_name:
                current_data = item[1]
                dialog = EditDialog(key_name, current_data, self)
                if dialog.exec():
                    for i in dialog.updated_data:
                        item[1][i] = dialog.updated_data[i]
                break
