from flask import Flask, request, jsonify, render_template, Response
from werkzeug.utils import secure_filename
import os
import json
import time
from chatwithpdf import DocumentChatbot
from summarizer import setup_conversation_memory, add_messages_to_history

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploaded_pdfs/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16MB

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/', methods=['GET'])
def home():
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
        return jsonify({'message': 'File uploaded successfully', 'path': pdf_path}), 200
    return jsonify({'error': 'File not allowed'}), 400


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    pdf_path = data.get('pdf_path', '')
    user_message = data.get('message', '').strip()
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    if not pdf_path or not os.path.exists(pdf_path):
        return jsonify({"error": "Invalid PDF path"}), 400

    chatbot = DocumentChatbot(model="gpt-3.5-turbo-0125", pdf_path=pdf_path)

    response = chatbot.chat(user_message, [])
    return jsonify({'response': response})


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['pdf']


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
