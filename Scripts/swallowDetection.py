# Kayla's Python Script

import cv2
import mediapipe as mp
import numpy as np
import time
import cv2
import mediapipe as mp
import numpy as np
import json
from datetime import datetime, timedelta

# Initialize MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)

# Open webcam
cap = cv2.VideoCapture(0)

# State variables
prev_frame = None
swallow_frames = []
frame_count = 0
last_event_time = None
cooldown_seconds = 2

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0]
        h, w, _ = frame.shape

        #Throat ROI (under chin)
        throat_indices = [14, 152, 164, 378, 200, 427, 411]
        throat_points = [(int(landmarks.landmark[i].x * w), int(landmarks.landmark[i].y * h)) for i in throat_indices]

        throat_mask = np.zeros((h, w), dtype=np.uint8)
        cv2.fillPoly(throat_mask, [np.array(throat_points, dtype=np.int32)], 255)
        throat_roi = cv2.bitwise_and(gray, gray, mask=throat_mask)

        #Upper face ROI (mouth + lower cheeks)
        upper_indices = list(range(48, 68)) + [1, 2, 3, 4, 5, 6, 7, 8]
        upper_points = [(int(landmarks.landmark[i].x * w), int(landmarks.landmark[i].y * h)) for i in upper_indices]

        upper_mask = np.zeros((h, w), dtype=np.uint8)
        cv2.fillPoly(upper_mask, [np.array(upper_points, dtype=np.int32)], 255)
        upper_roi = cv2.bitwise_and(gray, gray, mask=upper_mask)

        #Motion analysis
        if prev_frame is not None:
            prev_throat = cv2.bitwise_and(prev_frame, prev_frame, mask=throat_mask)
            prev_upper = cv2.bitwise_and(prev_frame, prev_frame, mask=upper_mask)

            diff_throat = cv2.absdiff(prev_throat, throat_roi)
            diff_upper = cv2.absdiff(prev_upper, upper_roi)

            _, thresh_throat = cv2.threshold(diff_throat, 20, 255, cv2.THRESH_BINARY)
            _, thresh_upper = cv2.threshold(diff_upper, 20, 255, cv2.THRESH_BINARY)

            motion_throat = np.sum(thresh_throat) / 255
            motion_upper = np.sum(thresh_upper) / 255

            print(f"Frame {frame_count}: Throat={motion_throat:.1f}, Upper={motion_upper:.1f}")

            #Swallow detection logic
            if motion_throat > 50 and motion_upper < 30:
                now = datetime.now()
                if not last_event_time or (now - last_event_time) > timedelta(seconds=cooldown_seconds):
                    timestamp = now.isoformat()
                    print(f"🫗 Swallow detected at frame {frame_count} ({timestamp})")
                    swallow_frames.append({
                        "frame": frame_count,
                        "timestamp": timestamp,
                        "motion_score_throat": motion_throat,
                        "motion_score_upper": motion_upper
                    })
                    last_event_time = now

        prev_frame = gray.copy()

        # Optional: show the ROI mask or debugging windows
        cv2.imshow("Throat ROI", throat_mask)
        cv2.imshow("Upper ROI", upper_mask)

    cv2.imshow("Swallow Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_count += 1

cap.release()
cv2.destroyAllWindows()

# Save events to JSON
with open("backend/swallowDetectionJson.json", "w") as f:
    json.dump(swallow_frames, f, indent=2)

print("✅ Swallow events saved to 'swallowDetectionJson.json'")


# In[ ]:




