import time
from getSpeechOperation import getOperation,setVoiceToText
from thread import start_new_thread

start_new_thread(setVoiceToText,())

while 1:
    time.sleep(1)
    print getOperation()
    #print resetVoiceToText()