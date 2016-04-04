import speech_recognition as sr
import subprocess
import time
import dht11
import RPi.GPIO as GPIO
import cv2
import forecastio
import requests
import json

auto_lights = False  # indicate if automatics lights are on or off


def check_movement():
    '''
    return 1 if movement someone's presence is detected
    else return 0
    '''
    GPIO.setup(2, GPIO.IN)
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    movement = GPIO.input(2)
    return movement


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
    TRIG = 23
    ECHO = 24

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


def check_door():
    '''
    takes a snap shot at the door and searches for a face and reports back
    '''
    subprocess.call(["fswebcam", "-r", "640x480", "test.jpg", "-S", "2"])
    #image_process = subprocess.Popen(["fswebcam", "-r", "640x480", "test.jpg", "-S", "2"])
    #image_process.wait()
    #subprocess.Popen(["xdg-open", "test.jpg"])
    face_cascade = cv2.CascadeClassifier('/home/pi/Home-Automation/Camera/haarcascade_frontalface_default.xml')
    img = cv2.imread('test.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    if(len(faces) == 0):
        return False

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    #cv2.imshow('img', img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    cv2.imwrite('output.jpg', img)
    return True


def increase_temperature():
    '''
    increases the temperature
    '''
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)

    # read data using pin 14
    instance = dht11.DHT11(pin=14)
    result = instance.read()
    while not result.is_valid():
        result = instance.read()

    print("temperature : " + str(result.temperature))
    speak("current temperature is " + str(result.temperature))
    speak("increasing temperature now..")


def decrease_temperature():
    '''
    deceases the temperature
    '''
    pass


def weather_forecast():
    '''
    Tells the current weather forecast
    '''
    API_KEY = "f5af7c9d5dcae926c4e5fcf75ea35dc6"

    send_url = "http://ip-api.com/json"

    r = requests.get(send_url)
    j = json.loads(r.text)

    latitude = j['lat']
    longitude = j['lon']
    print("current latitude, longitude is ", latitude, longitude)

    forecast = forecastio.load_forecast(API_KEY, latitude, longitude)
    datapoint = forecast.currently()

    print(datapoint.summary)
    print(datapoint.temperature)
    print(datapoint.precipProbability)
    speak("weather forecast says " + str(datapoint.summary))
    speak("Current temperature is " + str(datapoint.temperature) + "Celsius")
    speak("Probability of rainfall is " + str(datapoint.precipProbability * 100) + "percent")



if __name__ == "__main__":
    global auto_lights
    auto_lights = False
    r = sr.Recognizer()
    GPIO.setmode(GPIO.BCM)
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
                elif(command == "check"):
                    speak("checking the door")
                    if(check_door()):
                        speak("someone is at the door")
                        subprocess.Popen(["xdg-open", "output.jpg"])
                    else:
                        speak("there is no one at the door")
                elif(command == "increase temperature"):
                    speak("increasing temperature")
                    increase_temperature()
                elif(command == "decrease temperature"):
                    speak("decreasing temperature")
                    decrease_temperature()
                elif(command == "weather forecast"):
                    weather_forecast()
        except Exception as e:
                print("Error occured : ", e)
                speak("could not understand please repeat")