# db_manager.py
import sqlite3
from datetime import datetime, timedelta

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('pomodoro.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                duration INTEGER,
                session_type TEXT,
                completed_status BOOLEAN
            )
        ''')
        self.conn.commit()

    def start_session(self, session_type, duration):
        self.cursor.execute('''
            INSERT INTO sessions (start_time, session_type, duration)
            VALUES (?, ?, ?)
        ''', (datetime.now(), session_type, duration))
        self.conn.commit()

    def get_today_stats(self):
        today = datetime.now().date()
        self.cursor.execute('''
            SELECT 
                COUNT(*) as completed_sessions,
                COALESCE(SUM(duration)/60, 0) as total_minutes
            FROM sessions 
            WHERE date(start_time) = ? 
            AND completed_status = 1
            AND session_type = 'focus'
        ''', (today.strftime('%Y-%m-%d'),))
        
        result = self.cursor.fetchone()
        return {
            'completed_sessions': result[0] if result[0] else 0,
            'total_minutes': int(result[1] if result[1] else 0)
        }

    def get_historical_data(self, days=7):
        start_date = (datetime.now() - timedelta(days=days)).date()
        self.cursor.execute('''
            SELECT 
                date(start_time) as date,
                COALESCE(SUM(duration)/60, 0) as total_minutes
            FROM sessions
            WHERE date(start_time) >= ?
            AND completed_status = 1
            AND session_type = 'focus'
            GROUP BY date(start_time)
            ORDER BY date(start_time)
        ''', (start_date.strftime('%Y-%m-%d'),))
        
        return [
            {'date': row[0], 'total_minutes': int(row[1])} 
            for row in self.cursor.fetchall()
        ]

    def end_session(self, completed=False):
        self.cursor.execute('''
            UPDATE sessions 
            SET end_time = ?, completed_status = ?
            WHERE end_time IS NULL
        ''', (datetime.now(), completed))
        self.conn.commit()