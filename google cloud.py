import speech_recognition as sr
import json
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.record(source, duration=2)

with open("Unknown.json", "r") as f:
    credentials_json = f.read()
print(credentials_json)
try:
    print("Google Cloud Speech thinks you said " + r.recognize_google_cloud(audio, credentials_json=credentials_json, language="es-cl"))
except sr.UnknownValueError:
    print("Google Cloud Speech could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Cloud Speech service; {0}".format(e))