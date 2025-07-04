import cv2
import os
import numpy as np
import json

def train_model(dataset_dir="datasets", model_path="models/Trainer.yml"):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    current_id = 0
    x_train = []
    y_labels = []

    with open("detection/labels.json", "r") as f:
        labels = json.load(f)
        label_map = {v: int(k) for k, v in labels.items()}

    for name in os.listdir(dataset_dir):
        person_dir = os.path.join(dataset_dir, name)
        if not os.path.isdir(person_dir):
            continue

        label_id = label_map[name]

        for image_file in os.listdir(person_dir):
            img_path = os.path.join(person_dir, image_file)
            image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if image is None:
                continue
            x_train.append(image)
            y_labels.append(label_id)

    print(f"[INFO] Training on {len(x_train)} face samples...")
    recognizer.train(x_train, np.array(y_labels))
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    recognizer.save(model_path)
    print(f"[DONE] Model saved to {model_path}")

if __name__ == "__main__":
    train_model()
