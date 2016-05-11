import RPi.GPIO as GPIO
import dht11
import time
import datetime


def increase_temperature():
    '''
    increases the temperature
    '''
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)

    # read data using pin 14
    instance = dht11.DHT11(pin=17)
    result = instance.read()
    while not result.is_valid():
        result = instance.read()

    print("temperature : " + str(result.temperature))
    #speak("current temperature is " + str(result.temperature))
    #speak("increasing temperature now..")
    GPIO.setup(18, GPIO.OUT)

    GPIO.output(18, GPIO.LOW)
    time.sleep(2)
    print("yellow led on")
    GPIO.output(18, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(18, GPIO.LOW)

def decrease_temperature():
    '''
    deceases the temperature
    '''
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)

    # read data using pin 14
    instance = dht11.DHT11(pin=17)
    result = instance.read()
    while not result.is_valid():
        result = instance.read()

    print("temperature : " + str(result.temperature))
    #speak("current temperature is " + str(result.temperature))
    #speak("decreasing temperature now..")
    GPIO.setup(18, GPIO.OUT)

    GPIO.output(18, GPIO.LOW)
    time.sleep(2)
    print("yellow led on")
    GPIO.output(18, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(18, GPIO.LOW)

GPIO.setmode(GPIO.BCM)
increase_temperature()

time.sleep(3)

decrease_temperature()