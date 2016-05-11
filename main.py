import speech_recognition as sr
import subprocess
import time
import dht11
import RPi.GPIO as GPIO
import cv2
import os
import forecastio
import requests
import json
import imaplib
import email
from datetime import datetime
from datetime import timedelta
import pytz
import tzlocal
from bs4 import BeautifulSoup


def turn_on_led():
    '''
    Turns on the led
    '''
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, GPIO.HIGH)  # led on
    print("lights on")

def turn_off_led():
    '''
    Turns off the led
    '''
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, GPIO.LOW)  # led off
    print("lights off")

def speak(message):
    '''
    Speaks out the message
    '''
    #return #TODO remove this
    audio_stream = subprocess.Popen(["espeak", message])
    audio_stream.wait()



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

def toggle_yellow_led():
    GPIO.setup(18, GPIO.OUT)

    GPIO.output(18, GPIO.LOW)
    time.sleep(2)
    print("yellow led on")
    GPIO.output(18, GPIO.HIGH)
    time.sleep(2)
    print("yellow led off")
    GPIO.output(18, GPIO.LOW)

def increase_temperature():
    '''
    increases the temperature
    '''
    # read data using pin 14
    instance = dht11.DHT11(pin=17)
    result = instance.read()
    while not result.is_valid():
        result = instance.read()

    print("temperature : " + str(result.temperature))
    speak("current temperature is " + str(result.temperature) + " Celsuis. Increasing temperature")
    toggle_yellow_led()

def decrease_temperature():
    '''
    deceases the temperature
    '''
    # read data using pin 14
    instance = dht11.DHT11(pin=17)
    result = instance.read()
    while not result.is_valid():
        result = instance.read()

    print("temperature : " + str(result.temperature))
    speak("current temperature is " + str(result.temperature) + " Celsuis. decreasing temperature")
    toggle_yellow_led()


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

    message = "weather forecast says " + str(datapoint.summary) + ".\nCurrent temperature is " + str(datapoint.temperature) + "Celsius" + ".\nProbability of rainfall is " + str(datapoint.precipProbability * 100) + "percent"
    #speak("weather forecast says " + str(datapoint.summary))
    #speak("Current temperature is " + str(datapoint.temperature) + "Celsius")
    #speak("Probability of rainfall is " + str(datapoint.precipProbability * 100) + "percent")
    speak(message)

def get_time_difference(mail_time):
    '''
    tell the time difference from UTC to local timezone
    '''
    if(mail_time[24] == ' '):
        timediff = mail_time[25:][:5]
    elif(mail_time[25] == " "):
        timediff = mail_time[26:][:5]

    diff = timediff[0]
    hours = timediff[1:3]
    mins = timediff[3:5]

    return [diff, hours, mins]


def check_mail():
    '''
    checks your email for important tagged mails of the day
    '''
    print("fetching mail please wait..")
    list_of_mails = []
    mail = imaplib.IMAP4_SSL('imap.gmail.com', port=993)
    mail.login('abhyu195@gmail.com', 'cullingblade')
    # mail.select('[Gmail]/Drafts')
    # print(mail.list())

    mail.select("[Gmail]/Important")

    result, data = mail.search(None, "ALL")

    ids = data[0]
    id_list = ids.split()

    i = 1
    for email_id in reversed(id_list):
        result, data = mail.fetch(email_id, "(RFC822)")
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        local_timezone = tzlocal.get_localzone()
        date_format = "%a, %d %b %Y %H:%M:%S"
        current_date = datetime.now()

        # print("MAIL ", i)
        for item in email_message.items():
            if(item[0] == "Date"):
                mail_time = item[1][:24]
                utc_time = datetime.strptime(mail_time, date_format)
                timediff = get_time_difference(item[1])
                if(timediff[0] == '+'):
                    utc_time = utc_time - timedelta(hours=int(timediff[1]), minutes=int(timediff[2]))
                else:
                    utc_time = utc_time + timedelta(hours=int(timediff[1]), minutes=int(timediff[2]))
                local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
                # print(item[1])
                # print(local_time, local_time.day, local_time.month)
                # print(current_date, current_date.day, current_date.month)
                if(current_date.day == local_time.day and current_date.month == local_time.month):
                    read_mail = True
                else:
                    read_mail = False
                    break
            if(item[0] == "From"):
                mail_from = item[1]
                mail_from = mail_from[:mail_from.index('<')].strip()
            if(item[0] == "Subject"):
                mail_subject = item[1]

        if(read_mail):
            #print("MAIL " + str(i))
            #print(mail_from)
            #print(mail_subject)
            #speak("mail from " + mail_from + " with subject " + mail_subject)
            list_of_mails.append("mail from " + mail_from + " with subject " + mail_subject)
            i += 1
        else:
            break
    print('.\n'.join(list_of_mails))
    speak(".\n".join(list_of_mails))


def read_news():
    url = "https://news.google.co.in"

    r = requests.get(url)

    html = r.content
    soup = BeautifulSoup(html, "html.parser")

    headlines = soup.findAll("span",{"class":"titletext"})
    todays_news = []
    i = 0
    speak("Today's Headlines are")
    for headline in headlines:
        #print(headline.text)
        #speak(headline.text)
        todays_news.append(headline.text)
        i += 1
        if( i == 10):
            break
    print(".\n".join(todays_news))
    speak(".\n".join(todays_news))


def activate_security():
    global security_process
    intrusion_file = "/home/pi/Home-Automation/intrusion/intrusion.py"
    security_process = subprocess.Popen(["python", intrusion_file])#, stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
    print("Intrusion started")

def deactivate_security():
    global security_process
    security_process.kill()
    print("security deactivated")

def activate_auto_lights():
    global automatic_lights_process
    automatic_lights_file = "/home/pi/Home-Automation/IR/ir.py"
    automatic_lights_process = subprocess.Popen(["python", automatic_lights_file])#, stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    print("auto lights started")

def deactivate_auto_lights():
    global automatic_lights_process
    automatic_lights_process.kill()
    print("auto lights stopped")

automatic_lights_process = None
security_process = None

if __name__ == "__main__":
    r = sr.Recognizer()
    GPIO.setmode(GPIO.BCM)
    turn_off_led()
    activate_auto_lights()
    print("Automatic lights started")
    speak("good morning")
    while(True):
        #listen for command
        try:
            #with sr.Microphone() as source:
                #print("listening")
                #audio = r.listen(source)
                #print("done listening")
                #command = r.recognize_google(audio)
                #command = str(command)
                command = raw_input("enter command: ")
                print("you said " + str(command))
                if(command == "exit"):
                    speak("turning off")
                    break
                elif(command == "deactivate automatic lights"):
                    deactivate_auto_lights()
                elif(command == "activate security"):
                    turn_off_led()
                    deactivate_auto_lights()
                    activate_security()
                elif(command == "deactivate security"):
                    deactivate_security()
                    activate_auto_lights()
                elif(command == "good morning"):
                    speak("good morning to you too")
                elif(command == "turn on lights"):
                    deactivate_auto_lights()
                    speak("turning on the lights")
                    turn_on_led()
                elif(command == "turn off lights"):
                    activate_auto_lights()
                    speak("turning off the lights")
                    turn_off_led()
                elif(command == "increase temperature"):
                    speak("increasing temperature")
                    increase_temperature()
                elif(command == "decrease temperature"):
                    speak("decreasing temperature")
                    decrease_temperature()
                elif(command == "weather forecast"):
                    weather_forecast()
                elif(command == "check mail"):
                    speak("checking your mail")
                    check_mail()
                elif(command == "read news"):
                    read_news()
                else:
                    print("unknown command")
        except Exception as e:
                print("Error occured : ", e)
                speak("could not understand please repeat")