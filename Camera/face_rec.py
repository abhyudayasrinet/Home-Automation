import numpy as np
import cv2
from subprocess import call

call(["fswebcam", "-r","640x480","test.jpg","-S","2"])

#fswebcam -r 640x480 test.jpg -S 2

face_cascade = cv2.CascadeClassifier('/home/pi/Home-Automation/Camera/haarcascade_frontalface_default.xml')
#eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

img = cv2.imread('test.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, 1.1, 5)
print("faces", faces)

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    #roi_gray = gray[y:y+h, x:x+w]
    #roi_color = img[y:y+h, x:x+w]

cv2.imshow('img', img)
cv2.imwrite("output.jpg", img)
cv2.waitKey(0)
cv2.destroyAllWindows()