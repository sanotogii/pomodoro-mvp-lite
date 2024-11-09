# view_db.py
import sqlite3
from tabulate import tabulate
from datetime import datetime

def view_sessions():
    conn = sqlite3.connect('pomodoro.db')
    cursor = conn.cursor()
    
    print("\n=== Today's sessions check ===")
    today = datetime.now().date().strftime('%Y-%m-%d')
    cursor.execute('''
        SELECT 
            session_id,
            start_time,
            end_time,
            duration/60 as duration_minutes,
            session_type,
            completed_status
        FROM sessions
        WHERE date(start_time) = ?
    ''', (today,))
    
    today_rows = cursor.fetchall()
    if today_rows:
        print(f"Found {len(today_rows)} sessions for today ({today})")
        for row in today_rows:
            print(f"Session {row[0]}: Start={row[1]}, End={row[2]}, Duration={row[3]}min, Type={row[4]}, Completed={row[5]}")
    else:
        print(f"No sessions found for today ({today})")
    
    print("\n=== All sessions ===")
    cursor.execute('''
        SELECT 
            session_id,
            datetime(start_time) as start_time,
            datetime(end_time) as end_time,
            duration/60 as duration_minutes,
            session_type,
            completed_status
        FROM sessions
        ORDER BY start_time DESC
    ''')
    
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    
    print(tabulate(rows, headers=columns, tablefmt='grid'))
    
    conn.close()

if __name__ == '__main__':
    view_sessions()