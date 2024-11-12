import sys, os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFontDatabase, QFont
from pomodoro_app import PomodoroTimer
import platform

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Load fonts at application startup
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Platform-specific font paths
    if platform.system() == 'Darwin':  # macOS
        system_font = "SF Pro Display"
        fallback_font = ".AppleSystemUIFont"
    elif platform.system() == 'Windows':
        system_font = "Segoe UI"
        fallback_font = "Arial"
    else:  # Linux and others
        system_font = "Ubuntu"
        fallback_font = "DejaVu Sans"

    # Try to load custom fonts if available
    sf_font_path = os.path.join(current_dir, 'assets', 'font', 'SFCompactDisplay-Regular.otf')
    ny_font_path = os.path.join(current_dir, 'assets', 'font', 'NewYorkMedium-Regular.otf')
    
    sf_font_id = QFontDatabase.addApplicationFont(sf_font_path)
    ny_font_id = QFontDatabase.addApplicationFont(ny_font_path)
    
    # Use system fonts if custom fonts fail to load
    if sf_font_id == -1:
        print(f"Using system font: {system_font}")
        font_family = system_font
    else:
        families = QFontDatabase.applicationFontFamilies(sf_font_id)
        font_family = families[0] if families else system_font
    
    if ny_font_id == -1:
        ny_font_family = fallback_font
    else:
        ny_families = QFontDatabase.applicationFontFamilies(ny_font_id)
        ny_font_family = ny_families[0] if ny_families else fallback_font
        os.environ['POMO_NY_FONT_FAMILY'] = ny_font_family
    
    # Set application-wide default font
    app.setFont(QFont(font_family, 10))
    os.environ['POMO_FONT_FAMILY'] = font_family
    
    timer = PomodoroTimer()
    timer.show()
    sys.exit(app.exec())