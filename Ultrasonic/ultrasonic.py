import RPi.GPIO as GPIO
import time


def turn_pump_off(): #turn on led
    GPIO.setup(15, GPIO.OUT)
    GPIO.output(15, GPIO.LOW)
    print("turning pump off")
    GPIO.output(15, GPIO.HIGH)

def turn_pump_on(): #switch off led
    GPIO.setup(15, GPIO.OUT)
    GPIO.output(15, GPIO.LOW)
    print("turning pump on")
    GPIO.output(15, GPIO.LOW)


GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

print("Distance measurement in progress")

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)

print("waiting for sensor to settle")

time.sleep(2)

while True:

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()


    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150
    distance = round(distance, 2)

    print("distance is " + str(distance) + "cm")
    #GPIO.cleanup()

    if(distance < 6):
        turn_pump_off()
    else:
        turn_pump_on()
    time.sleep(3)