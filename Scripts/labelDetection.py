import cv2
import pytesseract
import time
import re
import subprocess
import os
from pytesseract import Output

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
script_dir = os.path.dirname(os.path.abspath(__file__))
analyze_script = os.path.join(script_dir, "analyze_text.py")

def preprocess_for_ocr(frame, use_clahe=True):
    """Preprocessing with optional CLAHE or simple blur."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if use_clahe:
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
    else:
        enhanced = gray

    resized = cv2.resize(enhanced, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    blurred = cv2.GaussianBlur(resized, (3, 3), 0)

    thresh = cv2.adaptiveThreshold(
        blurred, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 10
    )
    return thresh

def extract_high_confidence_text(image, conf_threshold=70):
    """Return high-confidence OCR text and bounding boxes."""
    data = pytesseract.image_to_data(image, output_type=Output.DICT)
    results, boxes = [], []

    for i in range(len(data['text'])):
        try:
            conf = int(data['conf'][i])
        except ValueError:
            continue
        text = data['text'][i].strip()
        if conf >= conf_threshold and text:
            if re.fullmatch(r'[A-Za-z0-9:.\-/]+', text):  # Looser match
                results.append(text)
                (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
                boxes.append((text, x, y, w, h))
    return results, boxes

# --- Config ---
cap = cv2.VideoCapture(0)
start_time = time.time()
last_detection_time = start_time
ocr_interval = 0.8
max_run_time = 30
min_run_time = 4
early_stop_gap = 8
last_ocr_time = 0
found_text = set()
last_boxes = []
show_thresh = False  # Press 't' to toggle showing the threshold view

print("⏳ Scanning for text...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    now = time.time()
    elapsed_total = now - start_time
    elapsed_since_last = now - last_detection_time

    if now - last_ocr_time >= ocr_interval:
        last_ocr_time = now

        # Always run OCR for now — disable motion filtering
        preprocessed = preprocess_for_ocr(frame, use_clahe=True)
        text_fragments, boxes = extract_high_confidence_text(preprocessed)

        new_texts = [txt for txt in text_fragments if txt not in found_text]
        if new_texts:
            found_text.update(new_texts)
            last_detection_time = now
            last_boxes = boxes
            print(f"✅ New text: {new_texts}")

    # Draw bounding boxes
    for (text, x, y, w, h) in last_boxes:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("📷 Camera", frame)

    if show_thresh:
        cv2.imshow("🔍 Preprocessed OCR View", preprocessed)

    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        print("❌ Manually exited.")
        break
    elif key & 0xFF == ord('t'):
        show_thresh = not show_thresh

    if elapsed_total >= max_run_time:
        print("🛑 Max time reached.")
        break
    if elapsed_total >= min_run_time and elapsed_since_last >= early_stop_gap:
        print("⚠️ No new text in 5 seconds. Stopping.")
        break

cap.release()
cv2.destroyAllWindows()

# Save results
if found_text:
    final_text = '\n'.join(sorted(found_text))
    with open('detected_text_output.txt', 'w') as f:
        f.write(final_text)
    print("💾 Saved to 'detected_text_output.txt'")
else:
    print("❗No text was detected.")


# calls the analyze_text.py script now that the txt file has been generate 
print("🚀 Launching analyze_text.py...")
subprocess.run(["python", analyze_script])