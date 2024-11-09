from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QSlider, QLabel)
from PyQt6.QtCore import Qt

class CompletionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.result = None
        self.duration = 5
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Session Complete')
        layout = QVBoxLayout(self)

        # Duration slider
        slider_layout = QHBoxLayout()
        self.duration_slider = QSlider(Qt.Orientation.Horizontal)
        self.duration_slider.setMinimum(5)
        self.duration_slider.setMaximum(120)
        self.duration_label = QLabel("5 minutes")
        slider_layout.addWidget(QLabel("Duration:"))
        slider_layout.addWidget(self.duration_slider)
        slider_layout.addWidget(self.duration_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        extend_btn = QPushButton("Extend Session")
        break_btn = QPushButton("Take Break")
        end_btn = QPushButton("End Session")
        
        button_layout.addWidget(extend_btn)
        button_layout.addWidget(break_btn)
        button_layout.addWidget(end_btn)

        layout.addLayout(slider_layout)
        layout.addLayout(button_layout)

        # Connect signals
        self.duration_slider.valueChanged.connect(self.updateDurationLabel)
        extend_btn.clicked.connect(self.extendSession)
        break_btn.clicked.connect(self.takeBreak)
        end_btn.clicked.connect(self.endSession)

    def updateDurationLabel(self, value):
        self.duration_label.setText(f"{value} minutes")
        self.duration = value

    def extendSession(self):
        self.result = "extend"
        self.accept()

    def takeBreak(self):
        self.result = "break"
        self.accept()

    def endSession(self):
        self.result = "end"
        self.reject()