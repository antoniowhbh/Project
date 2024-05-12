from flask import Flask, jsonify, request, render_template, session, redirect, url_for
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
import sqlite3
import os
import time
from werkzeug.security import generate_password_hash, check_password_hash
from chatbot import advisor_bot, course_scheduler
from summarizer import setup_conversation_memory, add_messages_to_history
from course_data import CourseManager  # Adjust according to your file structure
from chatwithpdf import DocumentChatbot

# Generate a random secret key
secret_key = os.urandom(24)

app = Flask(__name__)
app.secret_key = secret_key  # This should be a random, secret key in a production app
socketio = SocketIO(app)

history = []
waiting_for_confirmation = {}  # Dictionary to keep track of user session states

# Configuration for file uploads
app.config['UPLOAD_FOLDER'] = 'uploaded_pdfs/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16MB

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect('uniguide_student.db', timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def execute_db_query(query, args=()):
    retries = 5
    for _ in range(retries):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(query, args)
            conn.commit()
            return cur.lastrowid
        except sqlite3.OperationalError as e:
            if "locked" in str(e):
                time.sleep(0.1)
            else:
                raise
        finally:
            conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'status': 'error', 'message': 'Missing username or password'}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM StudentLogins WHERE Username = ?", (username,))
        student = cur.fetchone()
        conn.close()

        if student and check_password_hash(student['Password'], password):
            session['logged_in'] = True
            session['username'] = username
            return jsonify({'status': 'success', 'message': 'Logged in successfully!', 'redirect': url_for('dashboard')})
        else:
            return jsonify({'status': 'failure', 'message': 'Incorrect credentials'}), 401

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Notes WHERE StudentID = (SELECT StudentID FROM StudentLogins WHERE Username = ?)",
                (session.get('username'),))
    notes = cur.fetchall()
    conn.close()

    return render_template('dashboard.html', notes=notes)

@app.route('/note/save', methods=['POST'])
def save_note():
    if not session.get('logged_in'):
        return jsonify({'status': 'error', 'message': 'User not logged in'}), 403

    data = request.get_json()
    note_content = data.get('note_content')
    note_id = data.get('note_id', None)

    conn = get_db_connection()
    cur = conn.cursor()
    if note_id:
        cur.execute("UPDATE Notes SET NoteContent = ? WHERE NoteID = ?", (note_content, note_id))
    else:
        cur.execute("INSERT INTO Notes (StudentID, NoteContent) VALUES ((SELECT StudentID FROM StudentLogins WHERE Username = ?), ?)",
                    (session.get('username'), note_content))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success', 'message': 'Note saved successfully'})

@app.route('/note/auto_save', methods=['POST'])
def auto_save_note():
    note_content = request.get_json().get('note_content')
    session['auto_saved_note'] = note_content
    return jsonify({'status': 'success', 'message': 'Note auto-saved successfully'})

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        if not all([name, email, username, password]):
            return jsonify({'status': 'error', 'message': 'All fields are required'}), 400

        hashed_password = generate_password_hash(password)

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM StudentLogins WHERE Username = ?", (username,))
            if cur.fetchone():
                return jsonify({'status': 'error', 'message': 'Username already exists'}), 409

            cur.execute("INSERT INTO Students (StudentName, Major, Email) VALUES (?, ?, ?)", (name, 'Undeclared', email))  # Assuming Major is 'Undeclared'
            student_id = cur.lastrowid
            cur.execute("INSERT INTO StudentLogins (StudentID, Username, Password) VALUES (?, ?, ?)",
                        (student_id, username, hashed_password))
            conn.commit()
        except sqlite3.IntegrityError as e:
            conn.rollback()
            return jsonify({'status': 'error', 'message': 'Database error: ' + str(e)}), 500
        finally:
            conn.close()

        return jsonify({'status': 'success', 'message': 'Signup successful', 'redirect': url_for('login')})

@app.route('/courses', methods=['GET'])
def get_courses():
    manager = CourseManager('course_descriptions.txt')  # Adjust the path accordingly
    manager.load_courses()
    course_titles = manager.get_course_names_and_titles()
    return jsonify(course_titles)

@app.route('/chat')
def chat_index():
    return render_template('chat.html')

@socketio.on('connect')
def on_connect():
    emit('after connect', {'data': 'You are connected to the Chatbot!'})
    waiting_for_confirmation[request.sid] = False

@socketio.on('message')
def handle_message(data):
    user_message = data['message'].strip().lower()
    sid = request.sid
    if user_message == "quit":
        emit('response', {'data': 'Chatbot session ended.'})
        return
    if user_message == "confirm registration":
        emit('response', {'data': 'Please type "confirm" to proceed with registration, or "cancel" to cancel.'})
        waiting_for_confirmation[sid] = True
        return
    if waiting_for_confirmation.get(sid):
        handle_confirmation(user_message, sid)
        return
    process_normal_message(user_message)

def handle_confirmation(confirm, sid):
    if confirm == "confirm":
        final_input = ""
        generated_input = advisor_bot.answer("Provide final schedule in table format.", history)
        for chunk in generated_input:
            content = chunk.choices[0].delta.content if chunk.choices[0].delta.content is not None else ""
            final_input += content
        course_scheduler.schedule_class(f"Insert the following classes{final_input}")
        emit('response', {'data': 'Registration Submitted'})
    else:
        emit('response', {'data': 'Registration cancelled.'})
    waiting_for_confirmation[sid] = False

def process_normal_message(user_message):
    response = advisor_bot.answer(user_message, history)
    full_response = ""
    for chunk in response:
        content = chunk.choices[0].delta.content if chunk.choices[0].delta.content is not None else ""
        full_response += content
    history.append((user_message, full_response))
    emit('response', {'data': full_response})

@socketio.on('save_conversation')
def save_conversation(data):
    student_id = data.get('student_id')
    updated_history = add_messages_to_history(history)
    summary = setup_conversation_memory(updated_history).buffer

    query = """
        INSERT INTO Conversations (StudentID, ConversationSummary)
        VALUES (?, ?)
    """
    execute_db_query(query, (student_id, summary))

    emit('response', {'data': 'Conversation saved successfully!'})

@app.route('/upload', methods=['GET'])
def upload_page():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(pdf_path)
        session['pdf_path'] = pdf_path
        return jsonify({'message': 'File uploaded successfully', 'path': pdf_path}), 200
    return jsonify({'error': 'File not allowed'}), 400

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    pdf_path = session.get('pdf_path')
    user_message = data.get('message', '').strip()
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    if not pdf_path or not os.path.exists(pdf_path):
        return jsonify({"error": "Invalid PDF path"}), 400

    chatbot = DocumentChatbot(model="gpt-3.5-turbo-0125", pdf_path=pdf_path)

    response = chatbot.chat(user_message, [])
    return jsonify({'response': response})

@app.route('/download_notes')
def download_notes():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT NoteContent FROM Notes WHERE StudentID = (SELECT StudentID FROM StudentLogins WHERE Username = ?)",
                (session.get('username'),))
    notes = cur.fetchall()
    conn.close()

    notes_content = [note['NoteContent'] for note in notes]
    notes_file = os.path.join(app.config['UPLOAD_FOLDER'], f"{session.get('username')}_notes.txt")
    with open(notes_file, 'w') as f:
        for note in notes_content:
            f.write(note + "\n")

    return send_file(notes_file, as_attachment=True)

@app.route('/faq', methods=['GET'])
def faq():
    return render_template('faq.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
