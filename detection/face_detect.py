import cv2

def detect_faces(gray_frame, face_cascade):
    """
    Detects faces in a grayscale frame using Haar cascade.

    Args:
        gray_frame (np.ndarray): Grayscale image frame.
        face_cascade (cv2.CascadeClassifier): Preloaded Haar face detector.

    Returns:
        list: List of bounding boxes for each detected face.
    """
    faces = face_cascade.detectMultiScale(
        gray_frame,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(80, 80)
    )
    return faces
