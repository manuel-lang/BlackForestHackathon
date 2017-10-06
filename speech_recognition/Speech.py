#!/usr/bin/env python3                                                                                

import speech_recognition as sr
from thread import start_new_thread
import time

text = "r"

# get audio from the microphone                                                                       
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Speak:")
    audio = r.listen(source)

def getVoiceToText():
    global text
    while 1:
        time.sleep(1)
        try:
            text =  r.recognize_google(audio)
        except sr.UnknownValueError:
            print("Could not understand audio")

start_new_thread(getVoiceToText,())

while 1:
    time.sleep(1)
    print text