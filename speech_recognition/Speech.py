#!/usr/bin/env python3                                                                                

import speech_recognition as sr
from thread import start_new_thread
import time

text = "r"

def getVoiceToText():
    global text
    r = sr.Recognizer()
    m = sr.Microphone()
    while 1:
        print("ja")
        with m as source: audio = r.listen(source)
        try:
            text =  r.recognize_google(audio)
        except sr.UnknownValueError:
            print("Could not understand audio")

start_new_thread(getVoiceToText,())

while 1:
    time.sleep(1)
    print text