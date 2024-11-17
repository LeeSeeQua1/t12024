from PySide6.QtWidgets import QProgressBar
from PySide6.QtGui import QPainter, QPen


class CustomProgressBar(QProgressBar):
    def __init__(self, threshold, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.threshold = threshold

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)

        for level, color in self.threshold.items():
            pen = QPen(color, 4)
            painter.setPen(pen)

            rect = self.rect()
            threshold_position = rect.height() - (rect.height() * level / 100)

            painter.drawLine(rect.left() + 5, threshold_position, rect.right() - 5, threshold_position)
