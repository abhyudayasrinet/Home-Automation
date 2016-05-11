import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.IN)                            #Right sensor connection
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Left sensor connection


def turn_lights_on(): #turn on led
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, GPIO.LOW)
    print("turning lights on")
    GPIO.output(4, GPIO.HIGH)

def turn_lights_off(): #switch off led
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, GPIO.LOW)
    print("turning lights off")
    GPIO.output(4, GPIO.LOW)



while True:
          i=GPIO.input(2)                         #Reading output of right IR sensor
          if i==1:                                #Right IR sensor detects an object
               print "Obstacle detected"
               turn_lights_on()
          else:
               turn_lights_off()
               print("no obstacle")
          time.sleep(3)