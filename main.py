import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFontDatabase, QFont
from pomodoro_app import PomodoroTimer
import os

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Load fonts at application startup
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sf_font_path = os.path.join(current_dir, 'assets', 'font', 'SFCompactDisplay-Regular.otf')
    ny_font_path = os.path.join(current_dir, 'assets', 'font', 'NewYorkMedium-Regular.otf')
    
    # Load SF Compact Display font
    sf_font_id = QFontDatabase.addApplicationFont(sf_font_path)
    # Load New York font
    ny_font_id = QFontDatabase.addApplicationFont(ny_font_path)
    
    if sf_font_id == -1:
        print("Failed to load SF Compact Display font")
        font_family = "Arial"  # Fallback font
    else:
        families = QFontDatabase.applicationFontFamilies(sf_font_id)
        if families:
            font_family = families[0]
            print(f"Successfully loaded font: {font_family}")
        else:
            font_family = "Arial"  # Fallback font
            print("Font loaded but no family name found, using Arial")
    
    if ny_font_id == -1:
        print("Failed to load New York font")
        ny_font_family = "Arial"
    else:
        ny_families = QFontDatabase.applicationFontFamilies(ny_font_id)
        if ny_families:
            ny_font_family = ny_families[0]
            print(f"Successfully loaded New York font: {ny_font_family}")
            os.environ['POMO_NY_FONT_FAMILY'] = ny_font_family
        else:
            ny_font_family = "Arial"
            print("New York font loaded but no family name found, using Arial")
    
    # Set application-wide default font
    app.setFont(QFont(font_family, 10))
    
    # Store font family name for use in PomodoroTimer
    os.environ['POMO_FONT_FAMILY'] = font_family
    
    timer = PomodoroTimer()
    timer.show()
    sys.exit(app.exec())