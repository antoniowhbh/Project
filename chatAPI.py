from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from chatbot import advisor_bot, course_scheduler
import os
import sqlite3
from summarizer import setup_conversation_memory, add_messages_to_history

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
socketio = SocketIO(app)

history = []
waiting_for_confirmation = {}  # Dictionary to keep track of user session states


# Database connection function
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    return render_template('chat.html')


@socketio.on('connect')
def on_connect():
    emit('after connect', {'data': 'You are connected to the Chatbot!'})
    waiting_for_confirmation[request.sid] = False  # Initialize the state when user connects


@socketio.on('message')
def handle_message(data):
    user_message = data['message'].strip().lower()
    sid = request.sid  # Capture the session ID of the current user
    if user_message == "quit":
        emit('response', {'data': 'Chatbot session ended.'})
        return
    if user_message == "confirm registration":
        emit('response', {'data': 'Please type "confirm" to proceed with registration, or "cancel" to cancel.'})
        waiting_for_confirmation[sid] = True  # Set the flag to true when "confirm registration" is received
        return
    if waiting_for_confirmation.get(sid):  # Check if the user is supposed to confirm
        handle_confirmation(user_message, sid)
        return  # Ensure to return after handling to prevent fall-through
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
    waiting_for_confirmation[sid] = False  # Reset the flag after handling the confirmation


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
    student_id = data.get('student_id')  # Get student ID from the client side
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

    emit('response', {'data': 'Conversation saved successfully!'})


if __name__ == '__main__':
    socketio.run(app, debug=True)
