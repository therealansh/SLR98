"""
Created on Sun Nov 29 17:19:00 2020

@author: anshtyagi
"""

import os
import cv2
import sys

if not os.path.exists("CustomData/"):
    os.makedirs("CustomData/")

CUSTOM_DATA = "CustomData/"

GestureName = sys.argv[1]
GestureDest = "CustomData/"+sys.argv[1]

cam = cv2.VideoCapture(0)
count = 0

while True:
    
    ok,frame = cam.read()
    frame = cv2.flip(frame,1)

    cv2.rectangle(frame, (620 - 1, 9), (1020 + 1, 419), (555, 0, 0), 1)

    roi = frame[10:410,620:920]
    cv2.imshow("Frame", frame)


    gray = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    th3 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,5)
    ret, image = cv2.threshold(th3,20,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    cv2.imshow("Image",image)
    
    if cv2.waitKey(10) & 0xFF == ord('a'):
        cv2.imwrite(GestureDest+".jpg",image)
        # cv2.imwrite("test2.jpg",image)
        break
        
        
    if cv2.waitKey(1) & 0xFF == ord("q") or count==15 :
        break

cam.release()
cv2.destroyAllWindows()


