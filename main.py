import speech_recognition as sr
import subprocess
import time
import RPi.GPIO as GPIO


auto_lights = False  # indicate if automatics lights are on or off


def check_movement():
    '''
    return 1 if movement someone's presence is detected
    else return 0
    '''
    GPIO.setup(3, GPIO.IN)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    movement = GPIO.input(3)
    return movement


def turn_on_led():
    '''
    Turns on the led
    '''
    GPIO.setup(7, GPIO.OUT)
    GPIO.output(7, GPIO.HIGH)  # led on


def turn_off_led():
    '''
    Turns off the led
    '''
    GPIO.setup(7, GPIO.OUT)
    GPIO.output(7, GPIO.LOW)  # led off


def speak(message):
    '''
    Speaks out the message
    '''
    audio_stream = subprocess.Popen(["espeak", message])
    audio_stream.wait()


def check_water_level():
    '''
    check  if water level is almost at the top
    distance < 5cm
    '''
    TRIG = 16  # 23
    ECHO = 18  # 24

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG, False)

    time.sleep(2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150
    print("water level : ", distance)
    return round(distance, 2) < 6


if __name__ == "__main__":
    global auto_lights
    auto_lights = False
    r = sr.Recognizer()
    GPIO.setmode(GPIO.BOARD)
    while(True):
        if(auto_lights):  # check to switch on lights through auto lighting
            if(check_movement()):
                speak("turning on lights")
                turn_on_led()
            else:
                speak("turning off lights")
                turn_off_led()
        if(check_water_level()):
            speak("turning off water pump")
        #listen for command
        try:
            with sr.Microphone() as source:
                print("listening")
                audio = r.listen(source)
                print("done listening")
                command = r.recognize_google(audio)
                command = str(command)
                print("you said " + str(command))
                if(command == "quit"):
                    speak("turning off")
                    break
                elif(command == "turn on lights"):
                    speak("turning on the lights")
                    turn_on_led()
                elif(command == "turn off lights"):
                    speak("turning off the lights")
                    turn_off_led()
                elif(command == "turn on auto lights"):
                    auto_lights = True
                    speak("auto lights turned on")
                elif(command == "turn off auto lights"):
                    auto_lights = False
                    speak("auto lights turned off")
        except Exception as e:
                print("Error occured : ", e)
                speak("could not understand please repeat")

