import cv2
import os
import numpy as np

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
subjects = ["", "Manuel Lang", "Marius Bauer", "Tobias Oehler", "Jerome Klausmann"]

def detect_faces(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);
    if (len(faces) == 0):
        return None, None

    val = []
    for face in faces:
        (x, y, w, h) = face
        val.append(tuple((gray[y:y+w, x:x+h], face)))

    return np.asarray(val)

def prepare_training_data(data_folder_path):
    dirs = os.listdir(data_folder_path)
    faces = []
    labels = []
    for dir_name in dirs:
        if not dir_name.startswith("s"):
            continue;
        label = int(dir_name.replace("s", ""))
        subject_dir_path = os.path.join(data_folder_path, dir_name)
        subject_images_names = os.listdir(subject_dir_path)
        for image_name in subject_images_names:
            if image_name.startswith("."):
                continue;

            image_path = os.path.join(subject_dir_path, image_name)
            image = cv2.imread(image_path)
            for val in detect_faces(image):
                if val is None: continue
                face, rect = val
                if face is not None:
                    faces.append(face)
                    labels.append(label)
    
    return faces, labels

def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

def predict(test_img):
    img = test_img.copy()
    for val in detect_faces(img):
        if val is None: continue
        face, rect = val 
        label = face_recognizer.predict(face)
        label_text = subjects[label[0]]
        draw_rectangle(img, rect)
        draw_text(img, label_text, rect[0], rect[1]-5) 
    return img

def train():
    faces, labels = prepare_training_data("training")
    face_recognizer.train(faces, np.array(labels))

def test():
    img = cv2.imread('test/2.jpg')
    cv2.imshow('detection', predict(img))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def show_webcam(mirror=False):
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        if not img is None:
            if not ret_val: continue
            if mirror:
                img = cv2.flip(img, 1)
            try:
                cv2.imshow('detection', predict(img))
            except:
                cv2.imshow('detection', img)
            if cv2.waitKey(1) == 27: 
                break
            cv2.destroyAllWindows()

def main():
    train()
    test()
    #show_webcam(mirror=False)

if __name__ == '__main__':
    main()