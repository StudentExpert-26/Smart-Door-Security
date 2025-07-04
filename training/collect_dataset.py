import cv2
import os
import json

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def update_labels(name, labels_path="detection/labels.json"):
    if os.path.exists(labels_path):
        with open(labels_path, "r") as f:
            labels = json.load(f)
    else:
        labels = {}

    # Assign new ID if name not in labels
    if name not in labels.values():
        new_id = max(map(int, labels.keys()), default=-1) + 1
        labels[str(new_id)] = name
        with open(labels_path, "w") as f:
            json.dump(labels, f)
        return new_id
    else:
        # Return existing ID
        return next(int(k) for k, v in labels.items() if v == name)

def collect_dataset():
    name = input("Enter person's name: ").strip()
    user_id = update_labels(name)

    dataset_dir = f"datasets/{name}"
    ensure_dir(dataset_dir)

    face_cascade = cv2.CascadeClassifier("detection/haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(0)

    print(f"[INFO] Capturing images for: {name} (ID {user_id})")
    count = 0
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            file_path = f"{dataset_dir}/{count}.jpg"
            cv2.imwrite(file_path, face)
            count += 1

            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)
            cv2.putText(frame, f"{name} - {count}", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        cv2.imshow("Collecting", frame)
        if cv2.waitKey(1) & 0xFF == ord('q') or count >= 100:
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"[DONE] Collected {count} images for {name}")

if __name__ == "__main__":
    collect_dataset()
