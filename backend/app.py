from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import os
import json  # 👈 Needed for reading output_from_gpt.json
import cv2
import pytesseract
import base64
import numpy as np
from PIL import Image
import io
import threading

app = Flask(__name__)

# Enable CORS so React (on localhost:3000) can talk to Flask (on port 5050)
CORS(app, origins="http://localhost:3000")

# Global variable to track if webcam is running
webcam_running = False

@app.route('/run-script', methods=['GET'])
def run_script():
    print("🛰️ /run-script endpoint was hit!")

    # Resolve the absolute path to the labelDetection.py script
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Scripts/labelDetection.py'))
    print("📁 Resolved script path:", script_path)

    # Check if the file exists at that path
    if not os.path.exists(script_path):
        print("❌ Script file not found at:", script_path)
        return jsonify({'status': 'error', 'message': 'Script file not found'}), 404

    try:
        print("🚀 Launching script...")
        result = subprocess.run(['python3', script_path], capture_output=True, text=True)

        # Log the captured stdout and stderr from the script
        print("📤 Script stdout:\n", result.stdout)
        print("📥 Script stderr:\n", result.stderr)

        return jsonify({
            'status': 'success',
            'output': result.stdout,
            'errors': result.stderr
        })
    except Exception as e:
        print("❌ Error occurred while executing script:", e)
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# ✅ New route to get the saved GPT-parsed JSON
@app.route('/get-parsed-data', methods=['GET'])
def get_parsed_data():
    json_path = os.path.join(os.path.dirname(__file__), 'output_from_gpt.json')

    if not os.path.exists(json_path):
        return jsonify({'status': 'error', 'message': 'Parsed data not found'}), 404

    try:
        with open(json_path, 'r') as f:
            parsed_json = json.load(f)
        return jsonify({'status': 'success', 'data': parsed_json})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/detect-pill', methods=['POST'])
def detect_pill():
    try:
        # Get the base64 image from the request
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'status': 'error', 'message': 'No image provided'}), 400

        # Decode the base64 image
        image_data = base64.b64decode(data['image'].split(',')[1])
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to OpenCV format
        opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Save the image temporarily
        temp_image_path = os.path.join(os.path.dirname(__file__), 'temp_pill_image.jpg')
        cv2.imwrite(temp_image_path, opencv_image)

        # Run the pill detection script
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Scripts/pillDetection.py'))
        if not os.path.exists(script_path):
            return jsonify({'status': 'error', 'message': 'Pill detection script not found'}), 404

        result = subprocess.run(['python3', script_path, '--image', temp_image_path], capture_output=True, text=True)

        # Clean up the temporary file
        os.remove(temp_image_path)

        return jsonify({
            'status': 'success',
            'output': result.stdout,
            'errors': result.stderr
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/start-webcam', methods=['POST'])
def start_webcam():
    print("🛰️ /start-webcam endpoint was hit!")
    
    # Resolve the absolute path to the pillDetection.py script
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Scripts/pillDetection.py'))
    print("📁 Resolved script path:", script_path)

    # Check if the file exists at that path
    if not os.path.exists(script_path):
        print("❌ Script file not found at:", script_path)
        return jsonify({'status': 'error', 'message': 'Script file not found'}), 404

    try:
        print("🚀 Launching script...")
        result = subprocess.run(['python3', script_path], capture_output=True, text=True)

        # Log the captured stdout and stderr from the script
        print("📤 Script stdout:\n", result.stdout)
        print("📥 Script stderr:\n", result.stderr)

        return jsonify({
            'status': 'success',
            'output': result.stdout,
            'errors': result.stderr
        })
    except Exception as e:
        print("❌ Error occurred while executing script:", e)
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    # Run Flask on port 5050 so it doesn't collide with React's 3000
    app.run(debug=True, port=5050)
