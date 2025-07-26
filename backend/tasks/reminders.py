from celery import Celery
from celery.schedules import crontab
import sqlite3
import requests
import csv
from datetime import datetime, timedelta
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

celery = Celery('quiz_master', broker=os.environ.get('REDIS_URL', 'redis://localhost:6379/0'))
# Optional: if using result backend
celery.conf.result_backend = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

@celery.task
def send_daily_reminders():
    """Send daily reminders to users if inactive or if new quizzes are available"""
    conn = sqlite3.connect('quiz_master.db')
    c = conn.cursor()

    # Get quizzes created in last 24 hours
    yesterday = (datetime.now() - timedelta(days=1)).isoformat()
    c.execute('''
        SELECT id FROM quizzes WHERE date_of_quiz > ?
    ''', (yesterday,))
    new_quiz_ids = {row[0] for row in c.fetchall()}

    # Get all users
    c.execute("SELECT id, full_name, username FROM users WHERE role = 'user'")
    users = c.fetchall()

    reminders_sent = 0

    for user_id, full_name, email in users:
        # Has user taken any quiz in last 24h?
        c.execute('''
            SELECT COUNT(*) FROM scores
            WHERE user_id = ? AND timestamp > ?
        ''', (user_id, yesterday))
        recent_attempts = c.fetchone()[0]

        # Has user not taken any of the new quizzes?
        c.execute('SELECT quiz_id FROM scores WHERE user_id = ?', (user_id,))
        attempted_quizzes = {row[0] for row in c.fetchall()}
        missed_new_quizzes = new_quiz_ids - attempted_quizzes

        # Only notify if user is inactive or missed new quizzes
        if recent_attempts == 0 or missed_new_quizzes:
            message = f"""
            <h3>Hi {full_name},</h3>
            <p>We noticed you haven’t taken any quiz in the last 24 hours.</p>
            {"<p>There are also <strong>new quizzes</strong> you haven’t attempted yet.</p>" if missed_new_quizzes else ""}
            <p><a href="http://localhost:5173">Log in now</a> and keep up the practice!</p>
            """

            send_email(email, "📚 Daily Quiz Reminder", message)
            print(f"Reminder sent to {email}")
            reminders_sent += 1

    conn.close()
    return f"Reminders sent to {reminders_sent} users."

@celery.task
def generate_monthly_report():
    """Generate and email monthly quiz reports to all users"""
    conn = sqlite3.connect('quiz_master.db')
    c = conn.cursor()

    current_month = datetime.now().strftime('%Y-%m')

    # Get all users
    c.execute("SELECT id, full_name, username FROM users WHERE role = 'user'")
    users = c.fetchall()

    for user_id, full_name, email in users:
        # Fetch quiz stats for this user
        c.execute('''
            SELECT q.remarks, s.total_scored, s.timestamp
            FROM scores s
            JOIN quizzes q ON s.quiz_id = q.id
            WHERE s.user_id = ? AND s.timestamp LIKE ?
            ORDER BY s.timestamp
        ''', (user_id, f"{current_month}%"))
        
        scores = c.fetchall()
        quiz_count = len(scores)
        avg_score = sum(s[1] for s in scores) / quiz_count if quiz_count > 0 else 0

        # Generate HTML report
        html = f"<h2>Hi {full_name},</h2>"
        html += f"<p>Here's your <strong>monthly quiz report</strong> for {current_month}:</p>"
        html += f"<p><strong>Total Quizzes Taken:</strong> {quiz_count}</p>"
        html += f"<p><strong>Average Score:</strong> {avg_score:.1f}</p>"
        html += "<h3>Quiz Breakdown:</h3><table border='1' cellpadding='6'><tr><th>Quiz</th><th>Score</th><th>Date</th></tr>"

        for q_name, score, ts in scores:
            html += f"<tr><td>{q_name}</td><td>{score}</td><td>{ts}</td></tr>"

        html += "</table><p>Keep up the great work!</p>"

        # Send Email
        send_email(email, f"Monthly Quiz Report - {current_month}", html)

        print(f"Report sent to {email}")

    conn.close()
    return "Monthly reports sent to all users."

def send_email(to_email, subject, html_body):
    """Send an email using SMTP (update config for production)"""
    from_email = "derrickrds@gmail.com"  # change this
    from_password =os.environ.get('EMAIL_PASSWORD')

    msg = MIMEText(html_body, 'html')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    # SMTP Setup - update these for your email provider
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_email, from_password)
        server.send_message(msg)


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

celery.conf.beat_schedule = {
    'daily-reminders': {
        'task': 'tasks.reminders.send_daily_reminders',
        'schedule': crontab(hour=13, minute=35),
        #'schedule': crontab(minute='*/1'),  # every minute for testing
    },
    'monthly-user-report': {
        'task': 'tasks.reminders.generate_monthly_report',
        'schedule': crontab(day_of_month=1, hour=6, minute=0),
    },
}