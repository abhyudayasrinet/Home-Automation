
import cv2
from subprocess import call
import RPi.GPIO as GPIO
import time
import requests

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.IN)                            #Right sensor connection
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Left sensor connection


def capture_image():
    call(["fswebcam", "-r","640x480","test.jpg","-S","2"])

    #fswebcam -r 640x480 test.jpg -S 2

    face_cascade = cv2.CascadeClassifier('/home/pi/Home-Automation/Camera/haarcascade_frontalface_default.xml')
    #eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    img = cv2.imread('test.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    print("faces", faces)
    url = "http://www.eragon17.5gbfree.com/write_data.php"
    if(len(faces) > 0):
        print(len(faces))
        param =  { "intrusion" : len(faces) }
        r = requests.get(url, params = param)
        print(r.text)


while True:
          i=GPIO.input(2)                         #Reading output of right IR sensor
          if i==1:                                #Right IR sensor detects an object
               print "Intruder detected"
               capture_image()
          else:
              print("no intruders")
          time.sleep(3)



#for (x, y, w, h) in faces:
    #cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    ##roi_gray = gray[y:y+h, x:x+w]
    ##roi_color = img[y:y+h, x:x+w]

#cv2.imshow('img', img)
#cv2.imwrite("output.jpg", img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()