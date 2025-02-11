import httpx
import os
import json
from dotenv import load_dotenv
load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")  
API_URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {GROQ_API_KEY}"
}

data = {
    "messages": [
        {"role": "system", "content": "keep top_k = 5 and top_n = 5"},
        {"role": "user", "content": "prompt = 'Once upon a time in a land far, far away'\nvarying the value of top k and top n create answer in groqs chat completion api"}
    ],
    "max_tokens": 100,
    "top_k": 5,
    "top_p": 0.95,
    "num_return_sequences": 5,
    "temperature": 0.7

}
payload ={
    "model" : "llama-3.3-70b-versatile",
    "messages": [
        {"role": "system", "content": "keep top_k = 5 and top_n = 5"},
        {"role": "user", "content": "prompt = 'India is my country all indians "}
    ],
    # "parameters": {
        "max_tokens": 100,
        # "num_return_sequences": 5,
        "temperature": 0.7,
        # "top_k": 50,
        "top_p": 0.95,
        # "presence_penalty": 0.5,
        # "frequency_penalty": 0.5,
        # "length_penalty": 0.5,
        # "repetition_penalty": 0.5,
        # "early_stopping": True,
        # "stop_sequences": [".", "!"]
    # }
}

def make_api_call():
    response = httpx.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

if __name__ == "__main__":
    result = make_api_call()
    if result:
        print(result)
        print(json.dumps(result, indent=4))
