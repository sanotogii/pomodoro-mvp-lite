from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QColor, QPen

class CircularProgressBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.progress = 0
        self.timer_text = "00:00"
        self.setMinimumSize(300, 300)

    def setProgress(self, value):
        self.progress = value
        self.update()

    def setTimerText(self, text):
        self.timer_text = text
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw circle
        pen = QPen(QColor("#454545"))
        pen.setWidth(5)
        painter.setPen(pen)

        width = self.width()
        height = self.height()
        margin = 10
        rect = QRect(margin, margin, width - 2*margin, height - 2*margin)
        
        # Background circle
        painter.drawEllipse(rect)

        # Progress arc
        if self.progress > 0:
            pen.setColor(QColor("#4CAF50"))  # Green color for progress
            pen.setWidth(5)
            painter.setPen(pen)
            # Arc starts from 90 degrees (top) and moves clockwise
            # Convert progress (0-1) to degrees (0-360) and multiply by 16 (Qt requirement)
            span = int(-360 * self.progress * 16)  # Negative for clockwise
            painter.drawArc(rect, 90 * 16, span)

        # Timer text
        font = painter.font()
        font.setPointSize(min(width, height) // 9)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(QColor("#E0E0E0"))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.timer_text)