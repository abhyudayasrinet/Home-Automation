import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.IN)                            #Right sensor connection
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Left sensor connection
while True:
          i=GPIO.input(2)                         #Reading output of right IR sensor
          if i==1:                                #Right IR sensor detects an object
               print "Obstacle detected"
               time.sleep(0.1)
          #else:
               #print("no obstacle")
