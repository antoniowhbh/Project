from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
from chatwithpdf import DocumentChatbot
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # Assuming the DocumentChatbot class and model are imported and available here
            chatpdf = DocumentChatbot(model="gpt-3.5-turbo-0125", pdf_path=file_path)
            return 'File uploaded and processed successfully'
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
