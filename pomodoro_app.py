import sqlite3
from datetime import datetime
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QSlider, QLabel, QSystemTrayIcon, 
                            QMenu, QDialog, QStackedWidget)
from PyQt6.QtCore import Qt, QTimer, QRect
from PyQt6.QtGui import QPainter, QColor, QPen, QIcon
import win32gui
import win32con
import win32process
from components.circular_progress import CircularProgressBar
from components.stats_widget import StatsWidget
from components.completion_dialog import CompletionDialog
from database.db_manager import DatabaseManager
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import QUrl
import os

class PomodoroTimer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.setupSounds()
        self.initUI()
        self.setupSystemTray()
        
    def setupSounds(self):
        self.timer_sound = QSoundEffect()
        sound_path = os.path.join(os.path.dirname(__file__), 'assets', 'notification.wav')
        self.timer_sound.setSource(QUrl.fromLocalFile(sound_path))
        self.timer_sound.setVolume(1.0)

    def playTimerEndSound(self):
        self.timer_sound.play()

    def initUI(self):
        self.setWindowTitle('Pomodoro Timer')
        self.setStyleSheet(self.getStyleSheet())

        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)

        # Stacked Widget for Timer and Stats
        self.stacked_widget = QStackedWidget()
        
        # Timer Page
        self.timer_widget = QWidget()
        self.timer_layout = QVBoxLayout(self.timer_widget)
        self.setupTimerPage()
        
        # Stats Page
        self.stats_widget = StatsWidget(self.db)
        
        self.stacked_widget.addWidget(self.timer_widget)
        self.stacked_widget.addWidget(self.stats_widget)
        self.main_layout.addWidget(self.stacked_widget)

        # Navigation buttons
        nav_layout = QHBoxLayout()
        self.timer_btn = QPushButton("Timer")
        self.stats_btn = QPushButton("Stats")
        nav_layout.addWidget(self.timer_btn)
        nav_layout.addWidget(self.stats_btn)
        self.main_layout.addLayout(nav_layout)

        # Connect navigation signals
        self.timer_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.stats_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        self.resize(347, 749)

    def setupTimerPage(self):
        # Progress bar
        self.progress_bar = CircularProgressBar()
        self.timer_layout.addWidget(self.progress_bar)

        # Preset buttons
        presets_layout = QHBoxLayout()
        self.btn_25 = QPushButton("25 minutes")
        self.btn_50 = QPushButton("50 minutes")
        self.btn_25.setObjectName("presetButton")
        self.btn_50.setObjectName("presetButton")
        presets_layout.addWidget(self.btn_25)
        presets_layout.addWidget(self.btn_50)
        self.timer_layout.addLayout(presets_layout)
        # Custom duration slider
        slider_layout = QHBoxLayout()
        self.duration_slider = QSlider(Qt.Orientation.Horizontal)
        self.duration_slider.setMinimum(1)
        self.duration_slider.setMaximum(120)
        self.duration_label = QLabel("5 minutes")
        slider_layout.addWidget(QLabel("Duration:"))
        slider_layout.addWidget(self.duration_slider)
        slider_layout.addWidget(self.duration_label)
        self.timer_layout.addLayout(slider_layout)

        # Control buttons
        controls_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.pause_button = QPushButton("Pause")
        self.stop_button = QPushButton("Stop")
        self.start_button.setObjectName("controlButton")
        self.pause_button.setObjectName("controlButton")
        self.stop_button.setObjectName("controlButton")
        self.start_button.setProperty("buttonType", "start")
        self.pause_button.setProperty("buttonType", "pause")
        self.stop_button.setProperty("buttonType", "stop")
        controls_layout.addWidget(self.start_button)
        controls_layout.addWidget(self.pause_button)
        controls_layout.addWidget(self.stop_button)
        self.timer_layout.addLayout(controls_layout)

        # Connect signals
        self.duration_slider.valueChanged.connect(self.updateDurationLabel)
        self.start_button.clicked.connect(self.startTimer)
        self.pause_button.clicked.connect(self.pauseTimer)
        self.stop_button.clicked.connect(self.stopTimer)
        self.btn_25.clicked.connect(lambda: self.setPresetDuration(25))
        self.btn_50.clicked.connect(lambda: self.setPresetDuration(50))

        # Timer setup
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTimer)
        self.remaining_time = 0
        self.total_time = 0
        self.is_active = False
        self.session_type = "focus"

    def setupSystemTray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("assets/icon.png"))  # I will do this later
        
        tray_menu = QMenu()
        show_action = tray_menu.addAction("Show")
        quit_action = tray_menu.addAction("Quit")
        
        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(self.close)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def updateDurationLabel(self, value):
        self.duration_label.setText(f"{value} minutes")

    def setPresetDuration(self, minutes):
        self.duration_slider.setValue(minutes)

    def startTimer(self):
        if not self.is_active:
            self.total_time = self.duration_slider.value() * 60
            self.remaining_time = self.total_time
            self.db.start_session(self.session_type, self.total_time)
        self.timer.start(1000)
        self.is_active = True

    def pauseTimer(self):
        self.timer.stop()
        self.is_active = False

    def stopTimer(self):
        self.timer.stop()
        self.is_active = False
        self.remaining_time = 0
        self.progress_bar.setProgress(0)
        self.progress_bar.setTimerText("00:00")
        self.db.end_session(False)

    def updateTimer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            self.progress_bar.setTimerText(f"{minutes:02d}:{seconds:02d}")
            progress = 1 - (self.remaining_time / self.total_time)
            self.progress_bar.setProgress(progress)
        else:
            self.timer.stop()
            self.is_active = False
            self.db.end_session(True)
            self.playTimerEndSound()
            self.forceToFront()
            self.showCompletionDialog()

    def forceToFront(self):
        # Show and activate the window
        self.show()
        self.setWindowState((self.windowState() & ~Qt.WindowState.WindowMinimized) | Qt.WindowState.WindowActive)
        self.activateWindow()
        # Raise window to top and force focus
        self.raise_()
        
        # Get the window handle
        hwnd = self.winId().__int__()
        
        # Set window to foreground
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                             win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        # Remove the topmost flag
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                             win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        
        # Flash the taskbar icon
        win32gui.FlashWindow(hwnd, True)

    def showCompletionDialog(self):
        dialog = CompletionDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            if dialog.result == "extend":
                self.session_type = "focus"
                self.setPresetDuration(dialog.duration)
                self.startTimer()
            elif dialog.result == "break":
                self.session_type = "break"
                self.setPresetDuration(dialog.duration)
                self.startTimer()

    @staticmethod
    def getStyleSheet():
        return """
            QMainWindow {
                background-color: #000000;
            }
            QWidget {
                background-color: #1E1E1E;
                color: #E0E0E0;
            }
            QPushButton {
                background-color: #1E1E1E;
                border: 1px solid #E0E0E0;
                padding: 5px;
                min-width: 70px;
            }
            QPushButton:hover {
                background-color: #2E2E2E;
            }
            QSlider::groove:horizontal {
                border: 1px solid #E0E0E0;
                height: 4px;
            }
            QSlider::handle:horizontal {
                background: #E0E0E0;
                width: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }
            QPushButton#presetButton {
                background-color: #2E2E2E;
                border: 2px solid #4CAF50;
                border-radius: 15px;
                padding: 10px;
                min-width: 100px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton#presetButton:hover {
                background-color: #3E3E3E;
                border-color: #45a049;
            }
            QPushButton#presetButton:pressed {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton#controlButton {
                border-radius: 15px;
                padding: 8px;
                min-width: 80px;
                font-weight: bold;
                font-size: 13px;
            }
            
            QPushButton#controlButton[buttonType="start"] {
                background-color: #2E2E2E;
                border: 2px solid #4CAF50;
                color: #4CAF50;
            }
            QPushButton#controlButton[buttonType="start"]:hover {
                background-color: #4CAF50;
                color: white;
            }
            
            QPushButton#controlButton[buttonType="pause"] {
                background-color: #2E2E2E;
                border: 2px solid #FFA500;
                color: #FFA500;
            }
            QPushButton#controlButton[buttonType="pause"]:hover {
                background-color: #FFA500;
                color: white;
            }
            
            QPushButton#controlButton[buttonType="stop"] {
                background-color: #2E2E2E;
                border: 2px solid #FF4444;
                color: #FF4444;
            }
            QPushButton#controlButton[buttonType="stop"]:hover {
                background-color: #FF4444;
                color: white;
            }
            
            QPushButton#controlButton:pressed {
                padding: 10px;
            }
            QSlider::groove:horizontal {
                border: 1px solid #4CAF50;
                background: #2E2E2E;
                height: 10px;
                border-radius: 5px;
                margin: 2px 0;
            }

            QSlider::handle:horizontal {
                background: #4CAF50;
                border: none;
                width: 18px;
                height: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }

            QSlider::handle:horizontal:hover {
                background: #45a049;
            }

            QSlider::sub-page:horizontal {
                background: #4CAF50;
                border-radius: 5px;
            }

            QSlider::add-page:horizontal {
                background: #2E2E2E;
                border-radius: 5px;
            }

            QLabel {
                color: #E0E0E0;
                font-size: 13px;
                padding: 0 5px;
            }
        """