import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFontDatabase
from pomodoro_app import PomodoroTimer
import os

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Load font at application startup
    current_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(current_dir, 'assets', 'font', 'SFCompactDisplay-Regular.otf')
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id == -1:
        print(f"Failed to load font")
    
    timer = PomodoroTimer()
    timer.show()
    sys.exit(app.exec())