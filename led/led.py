import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
#GPIO.setwarnings(False)
GPIO.setup(7, GPIO.OUT)

print("led on")
GPIO.output(7, GPIO.HIGH)
time.sleep(2)
print("led off")
GPIO.output(7, GPIO.LOW)