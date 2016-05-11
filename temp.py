# -*- coding: utf-8 -*-

import subprocess
import time
import RPi.GPIO as GPIO
import time
#green led
GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
#GPIO.setup(4, GPIO.OUT)

def turn_on_led():
    '''
    Turns on the led
    '''
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, GPIO.HIGH)  # led on


def turn_off_led():
    '''
    Turns off the led
    '''
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, GPIO.LOW)  # led off


intrusion_file = "/home/pi/Home-Automation/intrusion/intrusion.py"
ir_file = "/home/pi/Home-Automation/IR/ir.py"
ultrasonic_file = "/home/pi/Home-Automation/Ultrasonic/ultrasonic.py"


#ultrasonic_stream = subprocess.Popen(["python", ultrasonic_file])#, stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
#time.sleep(5)
#print("Ultrasonic started")
#intrusion_stream = subprocess.Popen(["python", intrusion_file])#, stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
#time.sleep(5)
#print("Intrusion started")
ir_stream = subprocess.Popen(["python", ir_file])#, stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
time.sleep(5)
print("IR started")


while True:
    command = raw_input()
    if(command == "on"):
        turn_on_led()
    elif(command == "kill"):
        ir_stream.kill()
    else:
        turn_off_led()


    time.sleep(5)
