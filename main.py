import datetime
import os
import sys
import time
import webbrowser
import pyautogui
import pyttsx3
import speech_recognition as sr
import json
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import random
import numpy as np
import psutil
import subprocess
from deepseek_file_access import query_model  # Ensure this import is correct

# Initialize and load models, tokenizers, and other necessary components
with open("intents.json") as file:
    data = json.load(file)

model = load_model("chat_model.keras")

with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder = pickle.load(encoder_file)

# Function to initialize the speech engine
def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 50)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume + 0.25)
    return engine

def speak(text):
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()

# Function to listen to user input via microphone
def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening.......", end="", flush=True)
        r.pause_threshold = 1.0
        r.phrase_threshold = 0.3
        r.sample_rate = 48000
        r.dynamic_energy_threshold = True
        r.operation_timeout = 5
        r.non_speaking_duration = 0.5
        r.dynamic_energy_adjustment = 2
        r.energy_threshold = 4000
        r.phrase_time_limit = 10
        try:
            audio = r.listen(source)
            print("\rRecognizing......", end="", flush=True)
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except sr.WaitTimeoutError:
            print("\nNo input detected. Please try again.")
            return None
        except Exception as e:
            print("Say that again please")
            return None
    return query

# Function to query DeepSeek model and interact with the system
def handle_deepseek_query(query):
    if query is None:
        return
    
    response = query_model(query)  # DeepSeek model dynamically handles the query and returns the response
    speak(response)
    
    # Handle system interaction based on DeepSeek's response
    if "open" in response.lower():
        if "calculator" in response.lower():
            os.startfile('C:\\Windows\\System32\\calc.exe')
        elif "notepad" in response.lower():
            os.startfile('C:\\Windows\\System32\\notepad.exe')
        elif "paint" in response.lower():
            os.startfile('C:\\Windows\\System32\\mspaint.exe')
        elif "whatsapp" in response.lower():
            webbrowser.open("https://web.whatsapp.com/")
        elif "facebook" in response.lower():
            webbrowser.open("https://www.facebook.com/")
        else:
            speak("Sorry, I could not recognize the app to open.")
    
    elif "close" in response.lower():
        if "calculator" in response.lower():
            os.system("taskkill /f /im calc.exe")
        elif "notepad" in response.lower():
            os.system('taskkill /f /im notepad.exe')
        elif "paint" in response.lower():
            os.system('taskkill /f /im mspaint.exe')
        else:
            speak("Sorry, I could not recognize the app to close.")
    
    # Handle system condition queries like battery or CPU usage
    elif "system condition" in response.lower():
        usage = str(psutil.cpu_percent())
        speak(f"CPU is at {usage} percentage")
        battery = psutil.sensors_battery()
        percentage = battery.percent
        speak(f"System battery is at {percentage}%.")
        if percentage >= 80:
            speak("We have sufficient battery.")
        elif 40 <= percentage <= 75:
            speak("Consider connecting to a charger.")
        else:
            speak("Battery is low, please charge your system soon.")

# Main loop where Athena listens to commands and interacts with the system
if __name__ == "__main__":
    speak("Hello, I am Athena, your assistant. How can I help you today?")
    while True:
        query = command()
        if query is None:
            continue  # Skip this iteration if no query is detected

        query = query.lower()
        if 'exit' in query:
            speak("Exiting Athena. Goodbye!")
            sys.exit()

        handle_deepseek_query(query)
