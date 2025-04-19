from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import os
import json  # 👈 Needed for reading output_from_gpt.json
import cv2
import pytesseract

app = Flask(__name__)

# Enable CORS so React (on localhost:3000) can talk to Flask (on port 5050)
CORS(app, origins="http://localhost:3000")

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

if __name__ == '__main__':
    # Run Flask on port 5050 so it doesn't collide with React's 3000
    app.run(debug=True, port=5050)
