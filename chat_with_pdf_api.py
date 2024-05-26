from flask import Blueprint, request, jsonify, session
from werkzeug.utils import secure_filename
import os
from chatwithpdf import DocumentChatbot
from flask_cors import CORS

chat_with_pdf_api = Blueprint('chat_with_pdf_api', __name__)
CORS(chat_with_pdf_api, supports_credentials=True)

UPLOAD_FOLDER = 'uploaded_files'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

chatbot = None  # Global variable to store the chatbot instance

@chat_with_pdf_api.route('/upload', methods=['POST'])
def upload_file():
    # Check if the user is logged in
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'error': 'Unauthorized access'}), 401

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    global chatbot
    document_type = 'pdf' if filename.endswith('.pdf') else 'pptx' if filename.endswith('.pptx') else 'docx'
    chatbot = DocumentChatbot(model="gpt-3.5-turbo-0125", document_path=filepath, document_type=document_type)

    return jsonify({'message': 'File successfully uploaded', 'path': filepath}), 200

@chat_with_pdf_api.route('/chat', methods=['POST'])
def chat_with_bot():
    # Check if the user is logged in
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'error': 'Unauthorized access'}), 401

    data = request.get_json()
    query = data.get('message')
    if not query:
        return jsonify({'error': 'No message provided'}), 400
    if not chatbot:
        return jsonify({'error': 'No document loaded. Please upload a document first.'}), 400

    try:
        response = chatbot.chat(query)
        return jsonify({'response': response}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
