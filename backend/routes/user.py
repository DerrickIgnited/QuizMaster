from flask import Blueprint, request, jsonify, session
import sqlite3
import json
import redis
from .utils import cache_response
from werkzeug.security import check_password_hash, generate_password_hash

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
@cache_response('user_dashboard', timeout=60)
def dashboard():
    user_id = session['user_id']
    
    conn = sqlite3.connect('quiz_master.db')
    c = conn.cursor()
    
    # Get available quizzes
    c.execute('''
        SELECT q.id, q.chapter_id, q.date_of_quiz, q.time_duration, q.remarks,
            c.name as chapter_name, s.name as subject_name
        FROM quizzes q
        JOIN chapters c ON q.chapter_id = c.id
        JOIN subjects s ON c.subject_id = s.id
    ''')
    quizzes = c.fetchall()
    
    # Get user scores ordered by timestamp descending
    c.execute('''SELECT s.*, q.remarks as quiz_name, c.name as chapter_name 
        FROM scores s 
        JOIN quizzes q ON s.quiz_id = q.id 
        JOIN chapters c ON q.chapter_id = c.id 
        WHERE s.user_id = ? ORDER BY s.timestamp ASC''', (user_id,))
    scores = c.fetchall()
    
    conn.close()
    
    # Calculate average score
    total_scores = [s[4] for s in scores]
    average_score = (sum(total_scores) / len(total_scores))*100 if total_scores else 0
    
    # Prepare recent scores (limit to 5 most recent)
    recent_scores = [
        {'id': s[0], 'quiz_id': s[1], 'user_id': s[2],
         'timestamp': s[3], 'total_scored': s[4],
         'quiz_name': s[5], 'chapter_name': s[6]}
        for s in scores[:5]
    ]
    
    return jsonify({
        'quizzes': [
            {
                'id': q[0],
                'chapter_id': q[1],
                'date_of_quiz': q[2],
                'time_duration': q[3],
                'remarks': q[4],
                'chapter_name': q[5],
                'subject_name': q[6]
            }
            for q in quizzes
        ],
        'scores': [
            {'id': s[0], 'quiz_id': s[1], 'user_id': s[2],
             'timestamp': s[3], 'total_scored': s[4],
             'quiz_name': s[5], 'chapter_name': s[6]}
            for s in scores
        ],
        'recentScores': recent_scores,
        'averageScore': average_score
    })

@user_bp.route('/profile', methods=['GET', 'PUT'])
@login_required
@cache_response('user_profile', timeout=60)
def profile():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    if request.method == 'GET':
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

    elif request.method == 'PUT':
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Invalid input'}), 400

        username = data.get('username')
        full_name = data.get('full_name')
        qualification = data.get('qualification')
        dob = data.get('dob')

        if not all([username, full_name, qualification, dob]):
            return jsonify({'error': 'All fields are required'}), 400

        conn = sqlite3.connect('quiz_master.db')
        c = conn.cursor()
        c.execute('''
            UPDATE users
            SET username = ?, full_name = ?, qualification = ?, dob = ?
            WHERE id = ?
        ''', (username, full_name, qualification, dob, user_id))
        conn.commit()
        conn.close()

        return jsonify({
            'id': user_id,
            'username': username,
            'full_name': full_name,
            'qualification': qualification,
            'dob': dob
        })

@user_bp.route('/change-password', methods=['PUT'])
@login_required
@cache_response('user_changepassword', timeout=60)
def change_password():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.get_json()

    if not data:
        return jsonify({'message': 'Invalid input'}), 400

    current_password = data.get('current_password')
    new_password = data.get('new_password')

    if not current_password or not new_password:
        return jsonify({'message': 'Both current and new passwords are required'}), 400

    # Fetch the current hashed password from DB
    conn = sqlite3.connect('quiz_master.db')
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE id = ?', (user_id,))
    result = c.fetchone()

    if not result:
        conn.close()
        return jsonify({'message': 'User not found'}), 404

    stored_password_hash = result[0]

    # Verify current password
    if not check_password_hash(stored_password_hash, current_password):
        conn.close()
        return jsonify({'message': 'Incorrect current password'}), 403

    # Hash and update new password
    new_password_hash = generate_password_hash(new_password)

    c.execute('UPDATE users SET password = ? WHERE id = ?', (new_password_hash, user_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Password updated successfully'})
