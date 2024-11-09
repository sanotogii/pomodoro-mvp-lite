import sys
from PyQt6.QtWidgets import QApplication
from pomodoro_app import PomodoroTimer

if __name__ == '__main__':
    app = QApplication(sys.argv)
    timer = PomodoroTimer()
    timer.show()
    sys.exit(app.exec())