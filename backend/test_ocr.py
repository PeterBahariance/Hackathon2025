import cv2
import pytesseract
import numpy as np
import os

# Set the Tesseract path explicitly
tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = tesseract_path

print(f"Tesseract path: {tesseract_path}")
print(f"Tesseract exists: {os.path.exists(tesseract_path)}")

def test_ocr():
    try:
        # Create a simple test image with text
        img = np.zeros((100, 400, 3), dtype=np.uint8)
        cv2.putText(img, "TEST OCR", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Save the test image
        cv2.imwrite('test_image.png', img)
        print("Test image saved as 'test_image.png'")
        
        # Try to read the text
        print("Attempting OCR...")
        text = pytesseract.image_to_string(img)
        print("OCR Test Result:", text)
        return True
    except Exception as e:
        print("OCR Test Failed:", str(e))
        return False

if __name__ == "__main__":
    test_ocr() 