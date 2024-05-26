from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from chatwithpdf import DocumentChatbot

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploaded_files'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

chatbot = None  # Global variable to store the chatbot instance

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    global chatbot
    document_type = 'pdf' if filename.endswith('.pdf') else 'pptx' if filename.endswith('.pptx') else 'docx'
    chatbot = DocumentChatbot(model="gpt-3.5-turbo-0125", document_path=filepath, document_type=document_type)

    return jsonify({'message': 'File successfully uploaded', 'path': filepath}), 200

@app.route('/chat', methods=['POST'])
def chat_with_bot():
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

if __name__ == '__main__':
    app.run(debug=True)
