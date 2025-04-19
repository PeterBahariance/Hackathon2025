from flask import Blueprint, jsonify, request
import subprocess
import os
import pytesseract
import cv2
import numpy as np
import traceback

# Try to find Tesseract in common installation locations
tesseract_paths = [
    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    r'C:\Users\danny\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
]

for path in tesseract_paths:
    if os.path.exists(path):
        pytesseract.pytesseract.tesseract_cmd = path
        break
else:
    print("Warning: Tesseract not found in common locations. Please ensure it's installed and in PATH.")

bp = Blueprint('main', __name__)

@bp.route('/api/detect-label', methods=['POST'])
def detect_label():
    try:
        # Get the path to the labelDetection.py script
        # Go up two levels from backend/app/routes to reach the project root
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        script_path = os.path.join(base_dir, 'Scripts', 'labelDetection.py')
        
        print(f"Looking for script at: {script_path}")
        if not os.path.exists(script_path):
            return jsonify({
                'error': 'Script not found',
                'path': script_path
            }), 500
        
        # Run the script
        print("Running script...")
        result = subprocess.run(['python', script_path], capture_output=True, text=True)
        
        print(f"Script return code: {result.returncode}")
        print(f"Script stdout: {result.stdout}")
        print(f"Script stderr: {result.stderr}")
        
        if result.returncode != 0:
            return jsonify({
                'error': 'Detection failed',
                'details': result.stderr,
                'stdout': result.stdout
            }), 500
            
        # Read the output file
        output_path = os.path.join(base_dir, 'detected_text_output.txt')
        print(f"Looking for output at: {output_path}")
        
        if not os.path.exists(output_path):
            return jsonify({
                'error': 'Output file not found',
                'path': output_path
            }), 500
            
        with open(output_path, 'r') as f:
            detected_text = f.read()
            
        if not detected_text.strip():
            return jsonify({
                'error': 'No text was detected',
                'details': 'The camera did not detect any readable text'
            }), 400
            
        return jsonify({
            'success': True,
            'text': detected_text
        })
        
    except Exception as e:
        print(f"Error in detect_label: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@bp.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Backend is running!'}) 