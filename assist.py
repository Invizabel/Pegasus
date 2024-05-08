# requirements:
# anthropic
# instructor
# openai

from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List
import instructor
import json

# change these variables as needed
ai_model = "llama3"
my_ip = "127.0.0.1"

# keep these variables static
old_prompt = ""
old_response = ""

class My_Model(BaseModel):
    response: str

class My_Models(BaseModel):
    my_models: My_Model

def connect(prompt):
    global old_prompt

    api_key = "none"

    if len(old_prompt) > 0:
        new_prompt = f"your last prompt: {old_prompt} |  your last response: {old_response} | now respond with this current prompt: {prompt}"

    else:
        new_prompt = prompt

    try:
        client = instructor.from_openai(OpenAI(api_key = api_key, base_url = f"http://{my_ip}:11434/v1"), mode = instructor.Mode.JSON)

        gpt_response = client.chat.completions.create(messages = [{"role": "system", "content": new_prompt}], model = ai_model, response_model = My_Models, max_retries = 10)
        data = json.dumps(gpt_response.model_dump(), indent = 4)
        results = json.loads(data)["my_models"].items()

        old_prompt = prompt

        for key, value in results:
            return value

    except:
        return "I'm sorry, there is a problem connecting to the api! Please try again!"

def main():
    global old_response

    while True:
        prompt = input("prompt:\n")
        response = connect(prompt)
        print(response)
        old_response = response

if __name__ == "__main__":
    main()
