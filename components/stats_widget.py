from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime, timedelta

class StatsWidget(QWidget):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db = db_manager
        self.today_label = None
        self.pomodoros_label = None
        self.canvas = None
        self.initUI()
        self.setStyleSheet("""
            QWidget {
                background-color: #1E1E1E;
            }
            QLabel {
                color: #E0E0E0;
                font-size: 16px;
                padding: 10px;
            }
            QLabel#headerLabel {
                font-size: 24px;
                font-weight: bold;
                padding: 20px 10px;
            }
            QLabel#statsLabel {
                font-size: 18px;
                background-color: #2E2E2E;
                border-radius: 10px;
                padding: 15px;
                margin: 5px 10px;
            }
        """)

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QLabel("Statistics")
        header.setObjectName("headerLabel")
        layout.addWidget(header)
        
        # Today's stats in a container
        stats_container = QFrame()
        stats_container.setObjectName("statsLabel")
        stats_layout = QVBoxLayout(stats_container)
        
        today_stats = self.db.get_today_stats()
        self.today_label = QLabel("Today's Focus Time")
        self.today_label.setObjectName("statsLabel")
        self.pomodoros_label = QLabel(
            f"Completed Pomodoros: {today_stats['completed_sessions']}\n"
            f"Total Focus Time: {today_stats['total_minutes']} minutes"
        )
        self.pomodoros_label.setObjectName("statsLabel")
        
        layout.addWidget(self.today_label)
        layout.addWidget(self.pomodoros_label)

        # Configure matplotlib style
        plt.style.use('dark_background')
        fig, ax = plt.subplots(facecolor='#1E1E1E')
        ax.set_facecolor('#2E2E2E')
        
        self.canvas = FigureCanvas(fig)
        layout.addWidget(self.canvas)
        
        self.updateStats()

    def updateStats(self):
        today_stats = self.db.get_today_stats()
        self.today_label.setText("Today's Stats")
        self.pomodoros_label.setText(
            f"🎯 Completed Pomodoros: {today_stats['completed_sessions']}\n"
            f"⏱️ Total Focus Time: {today_stats['total_minutes']} minutes"
        )
        
        data = self.db.get_historical_data()
        
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        
        # Plot styling
        dates = [d['date'] for d in data]
        times = [d['total_minutes'] for d in data]
        
        bars = ax.bar(dates, times, color='#4CAF50', alpha=0.7)
        
        # Customize the plot
        ax.set_title('Daily Focus Time', color='#E0E0E0', pad=20, fontsize=14)
        ax.set_xlabel('Date', color='#E0E0E0', labelpad=10)
        ax.set_ylabel('Minutes', color='#E0E0E0', labelpad=10)
        
        # Style the grid
        ax.grid(True, linestyle='--', alpha=0.2)
        ax.spines['bottom'].set_color('#E0E0E0')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#E0E0E0')
        
        # Style the ticks
        ax.tick_params(colors='#E0E0E0', which='both')
        plt.xticks(rotation=45, ha='right')
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}m', ha='center', va='bottom', color='#E0E0E0')
        
        plt.tight_layout()
        self.canvas.draw()