from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # Import CORS
import os
import sqlite3
from chatbot import advisor_bot, course_scheduler
from summarizer import setup_conversation_memory, add_messages_to_history

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
CORS(app)  # Enable CORS on all routes for all origins

history = []
waiting_for_confirmation = {}  # Dictionary to keep track of user session states

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('uniguide_student.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/message', methods=['POST'])
def handle_message():
    data = request.json
    user_message = data['message'].strip().lower()
    # The SID is removed as it is unnecessary for stateless HTTP requests
    response = process_message(user_message)
    return jsonify({'data': response})

def process_message(user_message):
    if user_message == "quit":
        return 'Chatbot session ended.'
    elif user_message == "confirm registration":
        return 'Please type "confirm" to proceed with registration, or "cancel" to cancel.'
    else:
        return advisor_bot_answer(user_message)

def advisor_bot_answer(user_message):
    response = advisor_bot.answer(user_message, history)
    full_response = "".join(
        chunk.choices[0].delta.content if chunk.choices[0].delta.content is not None else ""
        for chunk in response
    )
    history.append((user_message, full_response))
    return full_response

@app.route('/save_conversation', methods=['POST'])
def save_conversation():
    data = request.json
    student_id = data.get('student_id')
    updated_history = add_messages_to_history(history)
    summary = setup_conversation_memory(updated_history).buffer

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Conversations (StudentID, ConversationSummary)
        VALUES (?, ?)
    """, (student_id, summary))
    conn.commit()
    conn.close()

    return jsonify({'data': 'Conversation saved successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
