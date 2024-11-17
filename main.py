import sys
from ui.entry import Window
from PySide6.QtWidgets import QApplication

from ui.mainWin import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # ex = Window()
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
