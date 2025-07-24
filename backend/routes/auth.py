from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import redis

auth_bp = Blueprint('auth', __name__)
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    conn = sqlite3.connect('quiz_master.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    
    if user and check_password_hash(user[2], password):
        session['user_id'] = user[0]
        session['role'] = user[6]
        return jsonify({
            'success': True,
            'user': {
                'id': user[0],
                'username': user[1],
                'full_name': user[3],
                'role': user[6]
            }
        })
    
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = generate_password_hash(data.get('password'))
    full_name = data.get('full_name')
    qualification = data.get('qualification', '')
    dob = data.get('dob', '')
    
    conn = sqlite3.connect('quiz_master.db')
    c = conn.cursor()
    
    try:
        c.execute('INSERT INTO users (username, password, full_name, qualification, dob) VALUES (?, ?, ?, ?, ?)',
                  (username, password, full_name, qualification, dob))
        conn.commit()
        return jsonify({'success': True, 'message': 'Registration successful'})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'message': 'Username already exists'}), 400
    finally:
        conn.close()

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})