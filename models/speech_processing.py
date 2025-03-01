import speech_recognition as sr
import pyttsx3
import threading

recognizer = sr.Recognizer()

import pyttsx3

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def speech_to_text():
    """Converts speech to text."""
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Could not understand audio."
        except sr.RequestError:
            return "Error connecting to speech recognition service."

if __name__ == "__main__":
    text_to_speech("Welcome to your interview. Please introduce yourself.")
    print("You said:", speech_to_text())
