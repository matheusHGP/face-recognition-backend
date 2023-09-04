import os
import cv2
import dlib
import numpy as np

from app.core.config import config


class FaceRecognize:

    def __init__(self, train_folder, recognize_folder, train_filename):
        self.train_folder = os.path.join(config.DATABASE_FOLDER, train_folder)

        self.recognize_folder = os.path.join(
            config.DATABASE_FOLDER, recognize_folder)

        self.train_filepath = os.path.join(
            config.DATABASE_FOLDER, train_filename)

        self.hog_classifier = dlib.get_frontal_face_detector()
        self.lbph_classifier = cv2.face.LBPHFaceRecognizer_create()

    def train_or_update_model(self, images_path):
        ids, faces = self.get_images_data(
            images_path
        )

        if os.path.isfile(self.train_filepath):
            self.update_model(ids, faces)
        else:
            self.train_model(ids, faces)

    def update_model(self, ids, faces):
        self.lbph_classifier.read(self.train_filepath)
        self.lbph_classifier.update(faces, ids)
        self.lbph_classifier.write(self.train_filepath)

    def train_model(self, ids, faces):
        self.lbph_classifier.train(faces, ids)
        self.lbph_classifier.write(self.train_filepath)

    def recognize(self, image_path):
        faces = self.get_faces(os.path.join(self.recognize_folder, image_path))
        predictions = []

        for face in faces:
            self.lbph_classifier.read(self.train_filepath)
            label, dist = self.lbph_classifier.predict(face)
            predictions.append(label)

        return predictions

    def get_faces(self, image_path, resize=(200, 200), zoom=20):
        image = cv2.imread(image_path)

        detections = self.hog_classifier(image)

        cropped_images = []

        for detection in detections:
            l, t = detection.left(), detection.top()
            r, b = detection.right(), detection.bottom()

            cropped_image = image[t + zoom:b - zoom, l + zoom:r-zoom]
            cropped_image = cv2.resize(cropped_image, resize)

            cropped_images.append(cv2.cvtColor(
                cropped_image, cv2.COLOR_BGR2GRAY))

        return cropped_images

    def get_images_data(self, images_path):
        new_path = os.path.join(self.train_folder, images_path)
        faces_files = [file for file in os.listdir(new_path)]

        ids = [int(images_path.split('-')[0])] * len(faces_files)
        faces = []

        for file in faces_files:
            path = new_path + f'/{file}'
            image = self.get_faces(path)[0]

            faces.append(image)

        return np.array(ids), faces
