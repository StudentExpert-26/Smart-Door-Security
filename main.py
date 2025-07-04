import cv2
import numpy as np
import os
import time
from datetime import datetime
import json

from detection.face_detect import detect_faces
from detection.blink_detector import detect_blink
from hardware.controller import unlock_door, deny_access, lock_door
from cloud.drive_uploader import upload_snapshot
from cloud.sheets_logger import log_to_google_sheets

# Load face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("models/Trainer.yml")

# Load label mappings
with open("detection/labels.json", "r") as f:
    labels = json.load(f)
    labels = {int(k): v for k, v in labels.items()}

# Constants
CONFIDENCE_THRESHOLD = 50
SNAPSHOT_DIR = "snapshots"
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

# Load Haar cascade
face_cascade = cv2.CascadeClassifier('detection/haarcascade_frontalface_default.xml')

# Start webcam
cap = cv2.VideoCapture(0)
print("[INFO] System initialized. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("[ERROR] Camera not available.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detect_faces(gray, face_cascade)

    blink_detected = detect_blink(frame)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        id_, confidence = recognizer.predict(roi_gray)

        if confidence < CONFIDENCE_THRESHOLD:
            name = labels.get(id_, "Unknown")
            access_granted = True
        else:
            name = "Unknown"
            access_granted = False

        # Blink-based anti-spoofing check
        if access_granted and not blink_detected:
            print("[WARNING] No blink detected – possible spoof.")
            access_granted = False
            name = "Spoof_Attempt"

        # Draw bounding box and label
        color = (0, 255, 0) if access_granted else (0, 0, 255)
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, f"{name} ({int(confidence)}%)", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        # Save snapshot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_path = os.path.join(SNAPSHOT_DIR, f"{name}_{timestamp}.jpg")
        cv2.imwrite(snapshot_path, frame)

        # Upload snapshot and log
        image_url = upload_snapshot(snapshot_path)
        log_to_google_sheets(name, confidence, image_url)

        # Trigger hardware
        if access_granted:
            unlock_door()
            time.sleep(3)
            lock_door()
        else:
            deny_access()

    cv2.imshow("SmartDoor AI - Face Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
