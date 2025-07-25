from flask import Blueprint, request, jsonify, session
import sqlite3
import json
import redis
from .utils import cache_response

admin_bp = Blueprint('admin', __name__)
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route('/dashboard', methods=['GET'])
@admin_required
@cache_response('admin_dashboard', timeout=60)
def admin_dashboard():
    conn = sqlite3.connect('quiz_master.db')
    c = conn.cursor()
    stats = {}
    c.execute('SELECT COUNT(*) FROM subjects')
    stats['subjects'] = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM chapters')
    stats['chapters'] = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM quizzes')
    stats['quizzes'] = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM users')
    stats['users'] = c.fetchone()[0]

    c.execute('SELECT * FROM subjects')
    subjects = [{'id': s[0], 'name': s[1], 'description': s[2]} for s in c.fetchall()]
    c.execute('SELECT * FROM chapters')
    chapters = [{'id': c[0], 'name': c[1], 'description': c[2], 'subject_id': c[3]} for c in c.fetchall()]
    c.execute('SELECT * FROM quizzes')
    quizzes = [{'id': q[0], 'chapter_id': q[1], 'date_of_quiz': q[2], 'time_duration': q[3], 'remarks': q[4]} for q in c.fetchall()]

    conn.close()
    return jsonify({
        'stats': stats,
        'subjects': subjects,
        'chapters': chapters,
        'quizzes': quizzes
    })

@admin_bp.route('/subjects', methods=['GET', 'POST'])
@admin_required
@cache_response('admin_subject', timeout=60)
def manage_subjects():
    conn = sqlite3.connect('quiz_master.db')
    c = conn.cursor()
    
    if request.method == 'POST':
        data = request.json
        c.execute('INSERT INTO subjects (name, description) VALUES (?, ?)',
                  (data['name'], data['description']))
        conn.commit()
        redis_client.delete('subjects_list')
        return jsonify({'success': True})
    
    # Check cache first
    cached_subjects = redis_client.get('subjects_list')
    if cached_subjects:
        return jsonify(json.loads(cached_subjects))
    
    c.execute('SELECT * FROM subjects')
    subjects = [{'id': s[0], 'name': s[1], 'description': s[2]} for s in c.fetchall()]
    
    # Cache for 5 minutes
    redis_client.setex('subjects_list', 300, json.dumps(subjects))
    conn.close()
    return jsonify(subjects)

@admin_bp.route('/chapters', methods=['GET', 'POST'])
@admin_required
@cache_response('admin_chapters', timeout=60)
def manage_chapters():
    conn = sqlite3.connect('quiz_master.db')
    c = conn.cursor()
    
    if request.method == 'POST':
        data = request.json
        c.execute('INSERT INTO chapters (name, description, subject_id) VALUES (?, ?, ?)',
                  (data['name'], data['description'], data['subject_id']))
        conn.commit()
        redis_client.delete(f'chapters_subject_{data["subject_id"]}')
        return jsonify({'success': True})
    
    c.execute('SELECT * FROM chapters')
    chapters = [{'id': c[0], 'name': c[1], 'description': c[2], 'subject_id': c[3]} for c in c.fetchall()]
    
    conn.close()
    return jsonify(chapters)

@admin_bp.route('/quizzes', methods=['GET', 'POST'])
@admin_required
@cache_response('admin_quizzes', timeout=60)
def manage_quizzes():
    conn = sqlite3.connect('quiz_master.db')
    c = conn.cursor()
    
    if request.method == 'POST':
        data = request.json
        c.execute('INSERT INTO quizzes (chapter_id, date_of_quiz, time_duration, remarks) VALUES (?, ?, ?, ?)',
                  (data['chapter_id'], data['date_of_quiz'], data['time_duration'], data['remarks']))
        conn.commit()
        return jsonify({'success': True})
    
    c.execute("""
        SELECT q.*, c.name as chapter_name, s.name as subject_name
        FROM quizzes q
        JOIN chapters c ON q.chapter_id = c.id
        JOIN subjects s ON c.subject_id = s.id;
    """)
    quizzes = [{ 'id': q[0], 'chapter_id': q[1], 'date_of_quiz': q[2], 'time_duration': q[3], 'remarks': q[4] , 'chapter_name': q[5], 'subject_name': q[6]} for q in c.fetchall()]
    
    conn.close()
    return jsonify(quizzes)

@admin_bp.route('/questions/<int:quiz_id>', methods=['GET', 'POST'])
@admin_required
@cache_response('admin_questions', timeout=60)
def manage_questions(quiz_id):
    conn = sqlite3.connect('quiz_master.db')
    c = conn.cursor()
    
    if request.method == 'POST':
        data = request.json
        c.execute('''INSERT INTO questions (quiz_id, question_statement, option1, option2, option3, option4, correct_answer) 
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (quiz_id, data['question_statement'], data['option1'], data['option2'], 
                   data['option3'], data['option4'], data['correct_answer']))
        conn.commit()
        return jsonify({'success': True})
    
    c.execute('SELECT * FROM questions WHERE quiz_id = ?', (quiz_id,))
    questions = [{'id': q[0], 'quiz_id': q[1], 'question_statement': q[2],
                 'option1': q[3], 'option2': q[4], 'option3': q[5], 'option4': q[6],
                 'correct_answer': q[7]} for q in c.fetchall()]
    
    conn.close()
    return jsonify(questions)

@admin_bp.route('/subjects/<int:subject_id>', methods=['DELETE'])
@admin_required
@cache_response('admin_subject', timeout=60)
def delete_subject(subject_id):
    print(subject_id)
    conn = sqlite3.connect('quiz_master.db')
    c = conn.cursor()
    c.execute('DELETE FROM subjects WHERE id = ?', (subject_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@admin_bp.route('/chapters/<int:chapter_id>', methods=['DELETE'])
@admin_required
@cache_response('admin_chapters', timeout=60)
def delete_chapter(chapter_id):
    conn = sqlite3.connect('quiz_master.db')
    c = conn.cursor()
    c.execute('DELETE FROM chapters WHERE id = ?', (chapter_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@admin_bp.route('/quizzes/<int:quiz_id>', methods=['DELETE'])
@admin_required
@cache_response('admin_quizzes', timeout=60)
def delete_quiz(quiz_id):
    conn = sqlite3.connect('quiz_master.db')
    c = conn.cursor()
    c.execute('DELETE FROM quizzes WHERE id = ?', (quiz_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@admin_bp.route('/questions/<int:question_id>', methods=['DELETE'])
@admin_required
@cache_response('admin_questions', timeout=60)
def delete_question(question_id):
    conn = sqlite3.connect('quiz_master.db')
    c = conn.cursor()
    c.execute('DELETE FROM questions WHERE id = ?', (question_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})