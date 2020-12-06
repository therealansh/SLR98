
"""
Created on Fri Nov 27 02:23:00 2020(rewrite)

@author: anshtyagi
"""

from lobe import ImageModel
import cv2
from PIL import Image
import os
from flask import Flask, render_template, Response, jsonify


class SLRModel(object):
    def __init__(self,model):
        self.loaded_model = ImageModel.load(model)

    def predict(self,img):
        self.result = self.loaded_model.predict(img)
        return self.result.prediction

model = SLRModel("models/signature.json")


def load_dataset():
    images = []
    CustomDataDest = "CustomData/"
    for file in os.listdir(CustomDataDest):
        if file.endswith(".jpg"):
            images.append(file)

    return images


def predict_custom_gesture(image):
    images = load_dataset()
    gestures_detected = {};
    for i in range(len(images)):
        img_to_compare = cv2.imread("CustomData/"+images[i])
        sift = cv2.SIFT_create()
        kp_1, desc_1 = sift.detectAndCompute(image, None)
        kp_2, desc_2 = sift.detectAndCompute(img_to_compare, None)

        index_params = dict(algorithm=0, trees=5)
        search_params = dict()
        flann = cv2.FlannBasedMatcher(index_params, search_params)

        matches = flann.knnMatch(desc_1, desc_2, k=2)

        good_points = []
        ratio = 0.6
        for m, n in matches:
            if m.distance < ratio * n.distance:
                good_points.append(m)
        num = 1
        num = min(len(kp_1),len(kp_2))
        if(num==0):
            num = 1
        percentage = len(good_points) / num * 100
        if(percentage>1):
            gesname = images[i]
            gesname = gesname.replace('.jpg', '')
            gestures_detected[gesname] = percentage

    return max(gestures_detected,key=gestures_detected.get,default=0)


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ok,frame = self.video.read()
        frame = cv2.flip(frame, 1)
        cv2.rectangle(frame, (620 - 1, 9), (1020 + 1, 419), (555, 0, 0), 1)
        roi = frame[10:410, 620:920]
        img = Image.fromarray(roi)
        pred = model.predict(img)
        print(pred)
        cv2.putText(frame,str(pred),(10, 150),cv2.FONT_HERSHEY_SIMPLEX,5,(255,255,0),2)

        _,jpeg = cv2.imencode('.jpg',frame)
        return jpeg.tobytes(),pred




    def get_custom_frame(self):
        ok,frame = self.video.read()
        frame = cv2.flip(frame, 1)
        cv2.rectangle(frame, (620 - 1, 9), (1020 + 1, 419), (555, 0, 0), 1)
        roi = frame[10:410, 620:920]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        th3 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 5)
        ret, image = cv2.threshold(th3, 20, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        img = cv2.resize(image, (300, 400))
        pred = predict_custom_gesture(img)
        if pred is None:
            pred = "0"
        cv2.putText(frame, str(pred), (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 255, 0), 2)
        _,jpeg = cv2.imencode('.jpg',frame)
        return jpeg.tobytes(),pred

app = Flask(__name__,template_folder="template")
camera = VideoCamera()

@app.route('/')
def index():
    return render_template('index.html',)

def gen(camera):
    while True:
        frame,pred = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n\r\n')

def custom_gen(camera):
    while True:
        frame, pred = camera.get_custom_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/image')
def predict():
    image,pred = camera.get_frame()
    return jsonify(pred)

@app.route('/custom')
def predict_custom():
    image,pred = camera.get_custom_frame()
    return jsonify(pred)

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/custom_frame')
def custom_video():
    return Response(custom_gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

