from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import redis
import json
from celery import Celery
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or 'quiz_master_secret_key_2024'
CORS(app, supports_credentials=True)

# Redis setup
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Celery setup
celery = Celery('quiz_master', broker='redis://localhost:6379/0')

# Database initialization
def init_db():
    conn = sqlite3.connect('quiz_master.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        full_name TEXT NOT NULL,
        qualification TEXT,
        dob TEXT,
        role TEXT DEFAULT 'user'
    )''')
    
    # Subjects table
    c.execute('''CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT
    )''')
    
    # Chapters table
    c.execute('''CREATE TABLE IF NOT EXISTS chapters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        subject_id INTEGER,
        FOREIGN KEY (subject_id) REFERENCES subjects (id)
    )''')
    
    # Quizzes table
    c.execute('''CREATE TABLE IF NOT EXISTS quizzes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chapter_id INTEGER,
        date_of_quiz TEXT,
        time_duration INTEGER,
        remarks TEXT,
        FOREIGN KEY (chapter_id) REFERENCES chapters (id)
    )''')
    
    # Questions table
    c.execute('''CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_id INTEGER,
        question_statement TEXT NOT NULL,
        option1 TEXT NOT NULL,
        option2 TEXT NOT NULL,
        option3 TEXT NOT NULL,
        option4 TEXT NOT NULL,
        correct_answer INTEGER NOT NULL,
        FOREIGN KEY (quiz_id) REFERENCES quizzes (id)
    )''')
    
    # Scores table
    c.execute('''CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_id INTEGER,
        user_id INTEGER,
        timestamp TEXT,
        total_scored INTEGER,
        FOREIGN KEY (quiz_id) REFERENCES quizzes (id),
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    # Create admin user
    admin_password = generate_password_hash('admin123')
    c.execute('INSERT OR IGNORE INTO users (username, password, full_name, role) VALUES (?, ?, ?, ?)',
              ('admin@quiz.com', admin_password, 'Quiz Master Admin', 'admin'))
    
    conn.commit()
    conn.close()

# Import routes
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.user import user_bp
from routes.quiz import quiz_bp

# Import chatbot blueprint
from routes.chatbot import chatbot_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(user_bp, url_prefix='/api/user')
app.register_blueprint(quiz_bp, url_prefix='/api/quiz')
app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=8001)
