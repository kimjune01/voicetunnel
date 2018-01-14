import speech_recognition
from gtts import gTTS
import os
import queue

import websocket
from threading import Thread
import threading
import time
from tempfile import TemporaryFile
import wave, sys, pyaudio
# import pygame

from enum import Enum

recognizer = speech_recognition.Recognizer()


class ClientState(Enum):
    Deciding = 0
    Speaking = 1
    Listening = 2
    Invalid = 99

def speak(incomingtext):
    print("In speak, incomingtext:")
    print(incomingtext)
    tts = gTTS(text=incomingtext, lang='en')
    tts.save("incomingtext.mp3")
    os.system("mplayer incomingtext.mp3")

    # pygame.mixer.init()
    # pygame.mixer.music.load("incomingtext.mp3")
    # pygame.mixer.music.play()
    # while pygame.mixer.music.get_busy() == True:
    #     continue

def listen():
    print("listen")
    with speech_recognition.Microphone() as source:
        # recognizer.energy_threshold = 700
        recognizer.adjust_for_ambient_noise(source, duration= 0.2)

        recognizer.dynamic_energy_threshold = True
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
            # print(recognizer.recognize_sphinx(audio))
            # return recognizer.recognize_sphinx(audio)
            recognized = recognizer.recognize_google(audio)
            return recognized
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
        except speech_recognition.UnknownValueError:
            print("Could not understand audio, trying again")
        except speech_recognition.RequestError as e:
            print("Recog Error; {0}".format(e))
        except speech_recognition.WaitTimeoutError:
            print("Timeout: speech_recognition.WaitTimeoutError")

    return ""

def on_error(ws, error):
    print(error)

def on_close(ws):
    speak("closed")
    print("### closed ###")

def on_message(ws, message):
    print('on_message: ', message)
    globalQueue.put(message)
    print('globalQueue size: ', globalQueue.qsize())

def hasIncomingMessage():
    return not globalQueue.empty()

def handleSpeakingState(ws):
    print("handleSpeakingState")
    while hasIncomingMessage():
        storedMessage = globalQueue.get()
        print('storedMessage from globalQueue: ',storedMessage)
        #TODO: investigate storing message in var, why does it work but direct call doesnt?
        speak(storedMessage)

    if globalQueue.empty():
        print('handleSpeakingState: queue is empty globalQueue is empty')
        # Speaking state complete, go back to deciding state
        handleDecidingState(ws)

def on_open(ws):
    # TODO Refactor
    clientState = ClientState.Deciding

    runThread = Thread(target=handleDecidingState, args=[ws])
    runThread.daemon = True
    runThread.start()

    Thread(target=ping).start()

def ping(*args):
    while True:
        time.sleep(1)
        ws.send("ping")


def handleDecidingState(ws):
    print("handleDecidingState")
    # TODO tune this time
    time.sleep(0.15)
    print("waited for 0.15 second before deciding")
    if hasIncomingMessage():
        # TODO Going into speaking state Refactor Later
        clientState = ClientState.Speaking
        handleSpeakingState(ws)
    else:
        # TODO Going into listening state Refactor later
        clientState = ClientState.Listening
        handleListeningState(ws)

def handleListeningState(ws):
    print("handleListeningState")
    raw = listen()
    if raw:
        print('raw: ', raw)
        ws.send(raw)
    # else raw is null, but we should still decide what to do
    handleDecidingState(ws)

if __name__ == "__main__":
    global globalQueue
    globalQueue = queue.Queue()

    host = "ws://voiceminder.localtunnel.me/websocket/"
    # host = "ws://localhost:5000/websocket/"
    ws = websocket.WebSocketApp(host,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
