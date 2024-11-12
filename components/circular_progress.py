from PyQt6.QtWidgets import QWidget, QSizePolicy
from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QFontDatabase
import os

class CircularProgressBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.progress = 0
        self.timer_text = "00:00"
        self.goal_text = ""
        self.setMinimumSize(300, 300)
        
        # Setting size policy to maintain aspect ratio
        self.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding,
            QSizePolicy.Policy.MinimumExpanding
        )
        self.ny_font_family = os.environ.get('POMO_NY_FONT_FAMILY', 'Arial')

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

    def setGoalText(self, text):
        self.goal_text = text
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
            pen.setColor(QColor("#4CAF50"))
            pen.setWidth(5)
            painter.setPen(pen)
            span = int(-360 * self.progress * 16)
            painter.drawArc(rect, 90 * 16, span)

        # Timer text with font
        font = painter.font()
        font.setFamily("SF Compact Display Regular")
        font.setPointSize(min(width, height) // 7)
        font.setBold(False)
        painter.setFont(font)
        painter.setPen(QColor("#E0E0E0"))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.timer_text)
        
        # Draw goal text below timer with New York font
        if self.goal_text:
            goal_font = QFont(self.ny_font_family)
            goal_font.setPointSize(min(width, height) // 14)
            painter.setFont(goal_font)
            goal_rect = QRect(rect.x(), rect.y() + rect.height()//2, rect.width(), rect.height()//2)
            painter.drawText(goal_rect, Qt.AlignmentFlag.AlignCenter, self.goal_text)