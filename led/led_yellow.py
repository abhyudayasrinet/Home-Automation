import RPi.GPIO as GPIO
import time
#green led
GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)

GPIO.output(18, GPIO.LOW)
time.sleep(2)
print("led on")
GPIO.output(18, GPIO.HIGH)
time.sleep(2)
print("led off")
GPIO.output(18, GPIO.LOW)