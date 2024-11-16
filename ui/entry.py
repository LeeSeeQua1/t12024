from PySide6.QtWidgets import QMainWindow, QTabWidget


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Zoo Database')
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu('File')
        self._controllers = []
