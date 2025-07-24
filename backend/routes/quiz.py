from flask import Blueprint, request, jsonify, session
import sqlite3
from datetime import datetime

quiz_bp = Blueprint('quiz', __name__)

def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Login required'}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@quiz_bp.route('/attempt/<int:quiz_id>', methods=['GET'])
@login_required
def get_quiz(quiz_id):
    conn = sqlite3.connect('quiz_master.db')
    c = conn.cursor()
    
    # Get quiz details
    c.execute('''SELECT q.*, c.name as chapter_name, s.name as subject_name 
                 FROM quizzes q 
                 JOIN chapters c ON q.chapter_id = c.id 
                 JOIN subjects s ON c.subject_id = s.id 
                 WHERE q.id = ?''', (quiz_id,))
    quiz = c.fetchone()
    
    # Get questions
    c.execute('SELECT id, question_statement, option1, option2, option3, option4 FROM questions WHERE quiz_id = ?', (quiz_id,))
    questions = c.fetchall()
    
    conn.close()
    
    return jsonify({
        'quiz': {
            'id': quiz[0],
            'chapter_name': quiz[5],
            'subject_name': quiz[6],
            'time_duration': quiz[3],
            'remarks': quiz[4]
        },
        'questions': [{'id': q[0], 'question_statement': q[1],
                      'option1': q[2], 'option2': q[3], 'option3': q[4], 'option4': q[5]} 
                     for q in questions]
    })

@quiz_bp.route('/submit/<int:quiz_id>', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    user_id = session['user_id']
    answers = request.json.get('answers', {})
    
    conn = sqlite3.connect('quiz_master.db')
    c = conn.cursor()
    
    # Get correct answers
    c.execute('SELECT id, correct_answer FROM questions WHERE quiz_id = ?', (quiz_id,))
    correct_answers = dict(c.fetchall())
    
    # Calculate score
    score = 0
    for question_id, user_answer in answers.items():
        if int(question_id) in correct_answers and correct_answers[int(question_id)] == user_answer:
            score += 1
    
    # Save score
    c.execute('INSERT INTO scores (quiz_id, user_id, timestamp, total_scored) VALUES (?, ?, ?, ?)',
              (quiz_id, user_id, datetime.now().isoformat(), score))
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'score': score,
        'total_questions': len(correct_answers)
    })