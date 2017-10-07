#!/usr/bin/env python
# -*- coding: utf-8 -*-

import speech_recognition as sr
from thread import start_new_thread
import time
from readConfig import config
import itertools
import operator

valueT = ""

def most_common(L):
  # get an iterable of (item, iterable) pairs
  SL = sorted((x, i) for i, x in enumerate(L))
  # print 'SL:', SLl
  groups = itertools.groupby(SL, key=operator.itemgetter(0))
  # auxiliary function to get "quality" for an item
  def _auxfun(g):
    item, iterable = g
    count = 0
    min_index = len(L)
    for _, where in iterable:
      count += 1
      min_index = min(min_index, where)
    # print 'item %r, count %r, minind %r' % (item, count, min_index)
    return count, -min_index
  # pick the highest-count/earliest item
  return max(groups, key=_auxfun)[0]

def setVoiceToText():
    r = sr.Recognizer()
    m = sr.Microphone()
    global valueT
    try:
        print("A moment of silence, please...")
        with m as source: r.adjust_for_ambient_noise(source)
        print("Set minimum energy threshold to {}".format(r.energy_threshold))
        while True:
            print("Say something!")
            with m as source: audio = r.listen(source)
            print("Got it! Now to recognize it...")
            try:
                # recognize speech using Google Speech Recognition
                value = r.recognize_google(audio)
                # we need some special handling here to correctly print unicode characters to standard output
                if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                    print(u"You said {}".format(value).encode("utf-8"))
                    valueT = value
                else:  # this version of Python uses unicode for strings (Python 3+)
                    print("You said {}".format(value))
                    valueT = value
            except sr.UnknownValueError:
                print("Oops! Didn't catch that")
            except sr.RequestError as e:
                print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
            getOperation()
    except KeyboardInterrupt:
        pass

def resetVoiceToText():
    global valueT
    valueT = ""
def getVoiceToText():
    global valueT
    return valueT

def openCalender():
    print 'test'

def getOperation():
    listErgebnis = []
    conf = config()
    listWords = conf.getList()
    listWord = []
    listWord2 = []
    listHappen = []
    operation2 = []
    i = 0
    voice = []
    voice = getVoiceToText()
    for item in listWords:
        for  secondItem in item:
            i += 1
            if i == 1:
                listWord.append(secondItem.split(','))
            if i == 2:
                listHappen.append(secondItem)
        i = 0
    listTest = voice.split(' ')
    for item in listWord:
        for item2 in listTest:
            if format(item2).encode("utf-8") in item:
                listErgebnis.append(item)
    try:
        operation = most_common(listErgebnis)
        i = listWord.index(operation)
    except ValueError:
        voice = ""
    if voice == "":
        print ''
    else:
        func_to_run = globals()[listHappen[i]]
        func_to_run()
        voice = ""










