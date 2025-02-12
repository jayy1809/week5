from groq import Groq
import os 
import httpx
from dotenv import load_dotenv
from typing import List, Dict
load_dotenv()

BASE_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

'''

When using Groq API, you can have more control over your model output by prefilling assistant messages. This technique gives you
the ability to direct any text-to-text model powered by Groq to:

Skip unnecessary introductions or preambles
Enforce specific output formats (e.g., JSON, XML)
Maintain consistency in conversations



'''


client = Groq(
    api_key = os.getenv("GROQ_API_KEY")
)





def make_groq_request(messages: List[Dict[str, str]], temperature: float = 0.7):

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    
    data = {
        "messages": messages,
        "model": "llama-3.3-70b-versatile",
        "temperature": temperature,
        "max_completion_tokens": 1000,
        # "response_format" : {"type": "json_object"}
    }
    
    try:
        with httpx.Client() as client:
            response = client.post(BASE_URL, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return None






completion = client.chat.completions.create(
    model="llama3-70b-8192",
    messages=[
        {
            "role": "user",
            "content": "Write a Python function to calculate the factorial of a number."
        },
        {
            "role": "assistant",
            "content": "```python"
        }
    ],
    stop="```",
)
print(completion)
print(completion.choices[0].message.content)
# for chunk in completion:
#     print(chunk)
#     print(chunk.choices[0].delta.content or "", end="")


completion_json = client.chat.completions.create(
    model="llama3-70b-8192",
    messages=[
        {
            "role": "user",
            "content": "Extract the title, author, published date, and description from the following book as a JSON object:\n\n\"The Great Gatsby\" is a novel by F. Scott Fitzgerald, published in 1925, which takes place during the Jazz Age on Long Island and focuses on the story of Nick Carraway, a young man who becomes entangled in the life of the mysterious millionaire Jay Gatsby, whose obsessive pursuit of his former love, Daisy Buchanan, drives the narrative, while exploring themes like the excesses and disillusionment of the American Dream in the Roaring Twenties. \n"
        },
        {
            "role": "assistant",
            "content": "```json"
        }
    ],
    stop="```",
)

print(completion_json)
print(completion_json.choices[0].message.content)


completion_xml = client.chat.completions.create(
    model="llama3-70b-8192",
    messages=[
        {
            "role": "user",
            "content": "Extract the title, author, published date, and description from the following book as a XML:\n\n\"The Great Gatsby\" is a novel by F. Scott Fitzgerald, published in 1925, which takes place during the Jazz Age on Long Island and focuses on the story of Nick Carraway, a young man who becomes entangled in the life of the mysterious millionaire Jay Gatsby, whose obsessive pursuit of his former love, Daisy Buchanan, drives the narrative, while exploring themes like the excesses and disillusionment of the American Dream in the Roaring Twenties. \n"
        },
        {
            "role": "assistant",
            "content": "```xml"  # even if we keep json here it is still giving us xml output
        }
    ],
    stop="```",
)

print(completion_xml)
print(completion_xml.choices[0].message.content)