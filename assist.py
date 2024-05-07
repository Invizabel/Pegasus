# requirements:
# anthropic
# instructor
# openai
# pyaudio
# pyttsx3
# SpeechRecognition

import pyttsx3
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List
import instructor
import json
import speech_recognition as sr

my_ip = "127.0.0.1"
old_prompt = ""
old_response = ""

def ears():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("GO")
        audio_text = r.listen(source)
        try:
            return r.recognize_google(audio_text)
        except:
             return None

def voice(content):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("rate", 150)
    engine.setProperty('voice', voices[1].id)
    engine.say(content)
    engine.runAndWait()

def connect(prompt):
    global old_prompt

    api_key = "none"

    class My_Model(BaseModel):
        response: str

    class My_Models(BaseModel):
        my_models: My_Model

    if len(old_prompt) > 0:
        new_prompt = f"your last prompt: {old_prompt} |  your last response: {old_response} | now respond with this current prompt: {prompt}"

    else:
        new_prompt = prompt

    client = instructor.from_openai(OpenAI(api_key = api_key, base_url = f"http://{my_ip}:11434/v1"), mode = instructor.Mode.JSON)

    gpt_response = client.chat.completions.create(messages = [{"role": "system", "content": new_prompt}], model = "llama3", response_model = My_Models, max_retries = 10)
    data = json.dumps(gpt_response.model_dump(), indent = 4)
    results = json.loads(data)["my_models"].items()

    old_prompt = prompt

    for key, value in results:
        return value

def main():
    global old_response

    while True:
        prompt = ears()

        if prompt == None:
            voice("Sorry, I did not get that")

        else:
            print(prompt)
            response = connect(prompt)
            print(response)
            old_response = response
            voice(response)

if __name__ == "__main__":
    main()
