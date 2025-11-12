print("📢 Starting Flask server...")

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from emotion_model import detect_emotion

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/detect-emotion', methods=['POST'])
def detect():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    file_path = os.path.join(UPLOAD_FOLDER, audio_file.filename)
    audio_file.save(file_path)

    try:
        emotion = detect_emotion(file_path)
        return jsonify({'emotion': emotion})
    except Exception as e:
        print("❌ Error detecting emotion:", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("📡 Running Flask now...")
    app.run(debug=True)
