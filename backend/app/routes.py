from flask import Blueprint, jsonify, request
import subprocess
import os
import pytesseract
import cv2
import numpy as np

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

bp = Blueprint('main', __name__)

@bp.route('/api/detect-label', methods=['POST'])
def detect_label():
    try:
        # Get the path to the labelDetection.py script
        script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Scripts', 'labelDetection.py')
        
        # Run the script
        result = subprocess.run(['python', script_path], capture_output=True, text=True)
        
        if result.returncode != 0:
            return jsonify({'error': 'Detection failed', 'details': result.stderr}), 500
            
        # Read the output file
        output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'detected_text_output.txt')
        with open(output_path, 'r') as f:
            detected_text = f.read()
            
        return jsonify({
            'success': True,
            'text': detected_text
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Backend is running!'}) 