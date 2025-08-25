from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import os
import nltk
from nltk.stem import WordNetLemmatizer
from models.intent_model import IntentClassifier
from utils.response_generator import generate_response
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Download NLTK data
nltk.download('punkt')
nltk.download('wordnet')

app = Flask(__name__, static_folder='static')

# Initialize the intent classifier
intent_classifier = IntentClassifier()

# Load intents data
with open('data/intents.json', 'r') as f:
    intents = json.load(f)

# Load education information
with open('data/education_info.json', 'r') as f:
    education_info = json.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    user_message = request.json['message']
    
    if not user_message:
        return jsonify({'response': 'Sorry, I didn\'t receive any message.'})
    
    # Predict the intent of the user message
    intent = intent_classifier.predict(user_message)
    
    # Generate appropriate response based on the intent
    response = generate_response(intent, user_message, education_info)
    
    return jsonify({'response': response})

# Ensure static files are properly served
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    # Create directories if they don't exist
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    if not os.path.exists('models/intent_model.h5'):
        intent_classifier.train()
    else:
        intent_classifier.load_model()
    
    app.run(debug=True)