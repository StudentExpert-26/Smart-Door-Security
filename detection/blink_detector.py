import cv2
import mediapipe as mp
import numpy as np

# Eye landmarks from MediaPipe Face Mesh
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False,
                                   max_num_faces=5,
                                   refine_landmarks=True,
                                   min_detection_confidence=0.5,
                                   min_tracking_confidence=0.5)

def eye_aspect_ratio(landmarks, eye_points):
    # Extract coordinates
    coords = np.array([(landmarks[i].x, landmarks[i].y) for i in eye_points])
    # Compute vertical and horizontal distances
    vertical1 = np.linalg.norm(coords[1] - coords[5])
    vertical2 = np.linalg.norm(coords[2] - coords[4])
    horizontal = np.linalg.norm(coords[0] - coords[3])
    ear = (vertical1 + vertical2) / (2.0 * horizontal)
    return ear

def detect_blink(frame, blink_threshold=0.23):
    """
    Returns True if a blink is detected in at least one face.
    """
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(img_rgb)
    if not results.multi_face_landmarks:
        return False

    for face_landmarks in results.multi_face_landmarks:
        left_ear = eye_aspect_ratio(face_landmarks.landmark, LEFT_EYE)
        right_ear = eye_aspect_ratio(face_landmarks.landmark, RIGHT_EYE)
        avg_ear = (left_ear + right_ear) / 2.0

        if avg_ear < blink_threshold:
            return True  # Blink detected
    return False
