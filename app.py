from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__)

# Set a secure and unique secret key
app.secret_key = os.urandom(24)  # Replace this with a real, randomly generated key

# Configure CORS for both /api/* and /auth/*
cors = CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "https://uniguide.com"],
        "supports_credentials": True
    },
    r"/auth/*": {  # Include CORS settings for auth paths
        "origins": ["http://localhost:3000", "https://uniguide.com"],
        "supports_credentials": True
    }
})

# Import the Blueprints
from chat_api import chat_api
from chat_with_pdf_api import chat_with_pdf_api
from auth_api import auth_api
from registration_api import registration_api
from conversation_api import conversation_api
from courses_api import courses_api  # Make sure the import path is correct

# Register the Blueprints with their respective URL prefixes
app.register_blueprint(chat_api, url_prefix='/chat')
app.register_blueprint(chat_with_pdf_api, url_prefix='/pdfchat')
app.register_blueprint(auth_api, url_prefix='/auth')
app.register_blueprint(registration_api, url_prefix='/registration')
app.register_blueprint(conversation_api, url_prefix='/conversations')
app.register_blueprint(courses_api, url_prefix='/api/courses')  # Adjust prefix if needed

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Specify host and port if needed
