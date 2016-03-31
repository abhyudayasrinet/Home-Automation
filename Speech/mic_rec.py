import speech_recognition as sr

r = sr.Recognizer()

while 1:
    try:
        with sr.Microphone() as source:
            print("listening")
            audio = r.listen(source)
            print("done listening")
            command = r.recognize_google(audio)
            print("you said " + str(command))
            if(command == "quit"):
                break
    except Exception as e:
            print("Error occured : ", e)