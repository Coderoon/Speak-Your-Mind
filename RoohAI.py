import os
import random
import speech_recognition as sr
import pyttsx3
import webbrowser
import openai
import datetime
from Config import apikey

chatStr = ""

def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"******: {query}\Nexi: " # Put enter you name inplace of sterick: "
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    speak(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAi Response for Prompt:  {prompt} \n **************************\n\n"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("OpenAi"):
        os.mkdir("OpenAi")

    with open(f"OpenAi/{''.join(prompt.split('intelligence')[1:])}.txt", "w") as f:
        f.write(text)

def speak(text, rate=150):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', rate)
        engine.setProperty('volume', 0.9)
        engine.say(text)
        engine.runAndWait()
    except Exception as e: 
        print(f"Error: {e}")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
        return query
    except Exception as e:
        return "Some Error has occurred. Sorry from Nexi" 

text_to_speak = "Hello, I am Nexi." 
speak(text_to_speak, rate=100)

while True:
    print("Listening.....")
    text = takeCommand()

    if "Open Youtube".lower() in text.lower():
        speak("Opening Youtube Sir.....")
        webbrowser.open("https://youtube.com")
    elif "Stop Yourself".lower() in text.lower():
        speak("Stopping myself Sir............")
        break
    elif "Using artificial Intelligence".lower() in text.lower():
        ai(prompt=text)
    else:
        chat(text)

    speak(text)
