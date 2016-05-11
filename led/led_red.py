import RPi.GPIO as GPIO
import time
#red led
GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
GPIO.setup(15, GPIO.OUT)

GPIO.output(15, GPIO.LOW)
time.sleep(2)
print("led on")
GPIO.output(15, GPIO.HIGH)
time.sleep(2)
print("led off")
GPIO.output(15, GPIO.LOW)