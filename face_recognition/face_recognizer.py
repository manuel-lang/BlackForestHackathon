import cv2
import os
import numpy as np
from localbinarypatterns import LocalBinaryPatterns
from sklearn.svm import LinearSVC
import dlib
from skimage import io
from sklearn.externals import joblib
from sklearn import preprocessing

subjects = ["", "Manuel Lang", "Marius Bauer", "Tobias Oehler", "Jerome Klausmann"]
desc = LocalBinaryPatterns(24, 8)

def detect_faces(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detector = dlib.get_frontal_face_detector()
    dets = detector(gray, 1)
    if (len(dets) == 0):
        return None, None
    val = []
    for i, d in enumerate(dets):
        y = d.top()
        x = d.left()
        w = d.right() - d.left()
        h = d.bottom() - d.top()
        val.append(tuple((gray[y:y+w, x:x+h], (x,y,w,h))))

    return np.asarray(val)

def prepare_training_data(data_folder_path):
    dirs = os.listdir(data_folder_path)
    data = []
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
                if val is None: 
                    print("LUL FAILED -_- ", os.path.join(dir_name, image_name))
                    continue
                face, rect = val
                if face is not None:
                    hist = desc.describe(face)
                    data.append(hist)
                    labels.append(label)

    return data, labels

def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_DUPLEX, 3, (255, 0, 0), 2)

def predict(test_img):
    model = joblib.load('svm_lbph.pkl')
    img = test_img.copy() 
    for val in detect_faces(img):
        if val is None: continue
        face, rect = val 
        hist = desc.describe(face).reshape(1, -1)
        label = model.predict(hist)[0]
        label_text = subjects[label]
        draw_rectangle(img, rect)
        draw_text(img, label_text, rect[0], rect[1]-5) 
    return img

def predict_labels(test_img):
    model = joblib.load('face_recognition/svm_lbph.pkl')
    img = test_img.copy()
    labels = []
    for val in detect_faces(img):
        if val is None: continue
        face, rect = val 
        hist = desc.describe(face).reshape(1, -1)
        label = model.predict(hist)[0]
        labels.append(subjects[label])
    return labels

def train():
    model = LinearSVC(C=100.0, random_state=42)
    data, labels = prepare_training_data("training")
    print("Training classifier ...")
    min_max_scaler = preprocessing.MinMaxScaler()
    data_scaled = min_max_scaler.fit_transform(data)
    model.fit(data, labels)
    print("Finished training ...")
    joblib.dump(model, 'svm_lbph.pkl', compress=9)

def test():
    img = cv2.imread('test/2.jpg')
    cv2.imshow('detection', cv2.resize(predict(img),(1700,1200)))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def init():
    train()
    test()

if __name__ == '__main__':
    init()