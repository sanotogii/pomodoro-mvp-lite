from PyQt6.QtWidgets import QWidget, QSizePolicy
from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtGui import QPainter, QColor, QPen

class CircularProgressBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.progress = 0
        self.timer_text = "00:00"
        self.setMinimumSize(300, 300)
        
        # Setting size policy to maintain aspect ratio
        self.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding,
            QSizePolicy.Policy.MinimumExpanding
        )

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        # Maintaining 1:1 aspect ratio
        return width

    def sizeHint(self):
        # Default square size
        return QSize(300, 300)

    def resizeEvent(self, event):
        side = min(self.width(), self.height())
        self.setGeometry(
            self.x() + (self.width() - side) // 2,
            self.y() + (self.height() - side) // 2,
            side,
            side
        )
        super().resizeEvent(event)

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
            # Arc starts at 90° (top) and moves clockwise. Qt uses a coordinate system where:
            # - 0° points right (3 o'clock position)
            # - 90° points up (12 o'clock position) 
            # - Angles increase counter-clockwise
            # Qt requires angles in 1/16th of a degree units, so we multiply by 16
            # Example: 90° * 16 = 1440 units in Qt's system
            span = int(-360 * self.progress * 16)  # Negative for clockwise
            painter.drawArc(rect, 90 * 16, span)

        # Timer text
        font = painter.font()
        font.setPointSize(min(width, height) // 9)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(QColor("#E0E0E0"))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.timer_text)