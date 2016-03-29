import speech_recognition as sr


def callback(rec, audio):
    command = rec.recognize_google(audio)
    print(command)


speech_recognizer = sr.Recognizer()
#print("wtf")
with sr.Microphone() as source:
    #print("start")
    audio = speech_recognizer.record(source, 4)
    print("done listening!")
    #speech_recognizer.listen_in_background(source, callback)
    #callback(speech_recognizer, audio)
    command = speech_recognizer.recognize_google(audio)
    print(command)
