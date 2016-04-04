import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
GPIO.setup(4, GPIO.OUT)

print("led on")
GPIO.output(4, GPIO.HIGH)
time.sleep(2)
print("led off")
GPIO.output(4, GPIO.LOW)