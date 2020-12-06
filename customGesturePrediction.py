"""
Created on Sun Nov 29 18:40:00 2020

@author: anshtyagi
"""

import os
import cv2
from skimage.measure import compare_ssim



def load_dataset():
    images = []
    CustomDataDest = "CustomData/"
    for file in os.listdir(CustomDataDest):
        if file.endswith(".jpg"):
            images.append(file)

    return images


def compare_images(img):
    images = load_dataset()
    for i in range(len(images)):
        img_to_compare= cv2.imread("CustomData/"+images[i])
        print(images[i])
        print(compare_ssim(img,img_to_compare,multichannel=True))


def predict(image):
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

# img = cv2.imread("test1.jpg")
# compare_images(img)

cam = cv2.VideoCapture(0)
while True:
    ok,frame = cam.read()
    frame = cv2.flip(frame,1)

    cv2.rectangle(frame, (620 - 1, 9), (1020 + 1, 419), (555, 0, 0), 1)

    roi = frame[10:410, 620:920]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    th3 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 5)
    ret, image = cv2.threshold(th3, 20, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    cv2.imshow("Frame",frame)

    img = cv2.resize(image,(300,400))
    print(predict(img))



    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()




