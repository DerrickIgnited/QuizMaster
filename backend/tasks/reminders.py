from celery import Celery
import sqlite3
import requests
import csv
from datetime import datetime, timedelta
import os

celery = Celery('quiz_master', broker='redis://localhost:6379/0')

@celery.task
def send_daily_reminders():
    """Send daily reminders to users"""
    conn = sqlite3.connect('quiz_master.db')
    c = conn.cursor()
    
    yesterday = (datetime.now() - timedelta(days=1)).isoformat()
    c.execute('''SELECT DISTINCT u.username, u.full_name 
                 FROM users u 
                 WHERE u.role = 'user' 
                 AND u.id NOT IN (
                     SELECT user_id FROM scores WHERE timestamp > ?
                 )''', (yesterday,))
    
    inactive_users = c.fetchall()
    
    for user in inactive_users:
        print(f"Sending reminder to {user[1]} ({user[0]})")
    
    conn.close()
    return f"Sent reminders to {len(inactive_users)} users"

@celery.task
def generate_monthly_report():
    """Generate monthly activity report"""
    conn = sqlite3.connect('quiz_master.db')
    c = conn.cursor()
    
    current_month = datetime.now().strftime('%Y-%m')
    c.execute('''SELECT u.full_name, COUNT(s.id) as quiz_count, 
                        AVG(s.total_scored) as avg_score
                 FROM users u 
                 LEFT JOIN scores s ON u.id = s.user_id 
                 WHERE s.timestamp LIKE ? OR s.timestamp IS NULL
                 GROUP BY u.id''', (f"{current_month}%",))
    
    report_data = c.fetchall()
    
    html_report = "<h1>Monthly Quiz Report</h1><table>"
    html_report += "<tr><th>User</th><th>Quizzes Taken</th><th>Average Score</th></tr>"
    
    for user_data in report_data:
        html_report += f"<tr><td>{user_data[0]}</td><td>{user_data[1] or 0}</td><td>{user_data[2] or 0:.1f}</td></tr>"
    
    html_report += "</table>"
    
    conn.close()
    print("Monthly report generated")
    return html_report

@celery.task
def export_user_performance_csv():
    """Export all users' quiz performance"""
    conn = sqlite3.connect('quiz_master.db')
    c = conn.cursor()

    c.execute('''
        SELECT u.username, u.full_name, s.quiz_id, s.total_scored, s.timestamp
        FROM users u
        JOIN scores s ON u.id = s.user_id
        ORDER BY u.username, s.timestamp
    ''')
    
    rows = c.fetchall()
    
    with open('exports/user_performance.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Username', 'Full Name', 'Quiz ID', 'Score', 'Timestamp'])
        writer.writerows(rows)

    conn.close()
    print("User performance CSV export completed")
    return "user_performance.csv generated successfully"

@celery.task
def export_user_quiz_history_csv(username):
    """Export quiz history for a specific user"""
    conn = sqlite3.connect('quiz_master.db')
    c = conn.cursor()

    c.execute('''
        SELECT u.username, s.quiz_id, s.total_scored, s.timestamp
        FROM users u
        JOIN scores s ON u.id = s.user_id
        WHERE u.username = ?
        ORDER BY s.timestamp
    ''', (username,))
    
    rows = c.fetchall()
    
    filename = f"exports/{username}_quiz_history.csv"
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Username', 'Quiz ID', 'Score', 'Timestamp'])
        writer.writerows(rows)

    conn.close()
    print(f"Quiz history exported for user: {username}")
    return f"{filename} generated successfully"

# Schedule tasks
celery.conf.beat_schedule = {
    'daily-reminders': {
        'task': 'tasks.reminders.send_daily_reminders',
        'schedule': 86400.0,  # Every 24 hours
    },
    'monthly-report': {
        'task': 'tasks.reminders.generate_monthly_report',
        'schedule': 2592000.0,  # Every 30 days
    },
}