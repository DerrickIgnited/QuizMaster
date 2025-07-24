from flask import Blueprint, request, jsonify, session
import sqlite3
import json
import redis

user_bp = Blueprint('user', __name__)
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Login required'}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@user_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    user_id = session['user_id']
    
    conn = sqlite3.connect('quiz_master.db')
    c = conn.cursor()
    
    # Get available quizzes
    c.execute('''SELECT q.*, c.name as chapter_name, s.name as subject_name 
                 FROM quizzes q 
                 JOIN chapters c ON q.chapter_id = c.id 
                 JOIN subjects s ON c.subject_id = s.id''')
    quizzes = c.fetchall()
    
    # Get user scores
    c.execute('''SELECT s.*, q.remarks, c.name as chapter_name 
                 FROM scores s 
                 JOIN quizzes q ON s.quiz_id = q.id 
                 JOIN chapters c ON q.chapter_id = c.id 
                 WHERE s.user_id = ?''', (user_id,))
    scores = c.fetchall()
    
    conn.close()
    
    return jsonify({
        'quizzes': [{'id': q[0], 'chapter_id': q[1], 'date_of_quiz': q[2],
                    'time_duration': q[3], 'remarks': q[4],
                    'chapter_name': q[5], 'subject_name': q[6]} for q in quizzes],
        'scores': [{'id': s[0], 'quiz_id': s[1], 'user_id': s[2],
                   'timestamp': s[3], 'total_scored': s[4],
                   'quiz_name': s[5], 'chapter_name': s[6]} for s in scores]
    })

@user_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    user_id = session['user_id']
    
    conn = sqlite3.connect('quiz_master.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    
    if user:
        return jsonify({
            'id': user[0],
            'username': user[1],
            'full_name': user[3],
            'qualification': user[4],
            'dob': user[5]
        })
    
    return jsonify({'error': 'User not found'}), 404