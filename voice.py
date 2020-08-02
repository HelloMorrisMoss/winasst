import speech_recognition as sr
import gtts as sp
import pyttsx3 as tts
import time
import asyncio

r = sr.Recognizer()
# s = sp.gTTS()
te = tts.init()
# te.say("Hello world.")
# te.setProperty('rate', 120)  # 120 words per minute
# te.setProperty('volume', 0.9)
# te.runAndWait()


def say(engine, msg):
    engine.say(words_from_audio)
    engine.runAndWait()


with sr.Microphone() as source:
    while True:
        print("Talk")
        # te.say("Speak now human.")
        te.setProperty('rate', 120)  # 120 words per minute
        te.setProperty('volume', 0.9)
        te.runAndWait()
        r.adjust_for_ambient_noise(source)
        audio_text = r.listen(source)
        print(audio_text)
        # print("Time over, thanks")
        # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling

        try:
            # using google speech recognition
            words_from_audio = r.recognize_sphinx(audio_text)
            # print(words_from_audio)
            if len(words_from_audio) > 0:
                # te.say(words_from_audio)
                # te.runAndWait()
                say(te, words_from_audio)
        except:
            print("Sorry, I did not get that")
            pass


def testing():
    r = sr.Recognizer()
    # s = sp.gTTS()
    te = tts.init()
    # te.say("Hello world.")
    # te.setProperty('rate', 120)  # 120 words per minute
    # te.setProperty('volume', 0.9)
    # te.runAndWait()

    with sr.Microphone() as source:

        # te.say("Words now human.")
        # te.runAndWait()
        # time.sleep(1.5)
        while True:
            print("Talk")
            te.say("Speak now human.")
            te.setProperty('rate', 120)  # 120 words per minute
            te.setProperty('volume', 0.9)
            te.runAndWait()
            audio_text = r.listen(source)
            print("Time over, thanks")
            # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling

            try:
                # using google speech recognition
                words_from_audio = r.recognize_google(audio_text)
                # print("Text: " + words_from_audio)
                te.say(words_from_audio)
                # te.say("words")
                # te.setProperty('rate', 500)  # 120 words per minute
                # te.setProperty('volume', 0.9)
                te.runAndWait()
            except:
                print("Sorry, I did not get that")
