import httpx
import json
from typing import Dict, Any
import time
import os 
from dotenv import load_dotenv
import asyncio
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")  
BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

def make_groq_request(messages: list, **params) -> Dict[Any, Any]:
    """
    Make a request to Groq API with specified parameters
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    
    data = {
        "messages": messages,
        "model": "llama-3.3-70b-versatile", 
        **params
    }
    
    try:
        with httpx.Client() as client:
            response = client.post(BASE_URL, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return None
    



def stream_groq_response(messages: list, **params) -> None:
    """
    Stream response from Groq API
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    
    data = {
        "messages": messages,
        "model": "llama2-70b-4096",
        "stream": True,
        **params
    }
    
    try:
        with httpx.Client() as client:
            with client.stream("POST", BASE_URL, headers=headers, json=data) as response:
                response.raise_for_status()
                for chunk in response.iter_bytes():
                    chunk_str = chunk.decode("utf-8")

                    for line in chunk_str.splitlines():
                        if not line.strip():
                            continue

                        if line.startswith("data: "):
                            try:
                                chunk_data = json.loads(line[6:])
                                if chunk_data.get("choices"):
                                    content = chunk["choices"][0].get("delta", {}).get("content", "")
                                    if content:
                                        print(content, end="", flush=True)
                            except json.JSONDecodeError:
                                continue
    except httpx.HTTPError as e:
        print(f"HTTP error occurred: {e}")

# Example messages
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Write a short story about a magical forest."}
]


# Example 1: Basic request with default parameters
print("\n=== Example 1: Default Parameters ===")
s1 = time.time()
response = make_groq_request(
    messages,
    temperature=0.7,
    max_completion_tokens = 1024,
    top_p=0.9,
    # top_k=40
)
print(json.dumps(response, indent=2))
print("Time taken: ", time.time()-s1)


# Example 2: High temperature for more creative output
s2 = time.time()
print("\n=== Example 2: High Temperature (1.5) ===")
response = make_groq_request(
    messages,
    temperature=1.5,
    max_completion_tokens=1024,
    top_p=0.9,
    # top_k=40
)
print(json.dumps(response, indent=2))
print("Time taken: ", time.time()-s2)

# Example 3: Using stop sequences
print("\n=== Example 3: With Stop Sequences ===")
s3 = time.time()
response = make_groq_request(
    messages,
    temperature=0.7,
    max_completion_tokens=1024,
    stop=[".", "!", "?"],  # Will stop at first sentence
    top_p=0.9,
    # top_k=40
)
print(json.dumps(response, indent=2))
print("Time taken: ", time.time()-s3)

# Example 4: Very focused output (low temperature, low top_p, low top_k)
s4 = time.time()
print("\n=== Example 4: Focused Output ===")
response = make_groq_request(
    messages,
    temperature=0.3,
    max_completion_tokens=1024,
    top_p=0.5,
    # top_k=10
)
print(json.dumps(response, indent=2))
print("Time taken: ", time.time()-s4)

# Example 5: Streaming example
print("\n=== Example 5: Streaming Response ===")
s5 = time.time()
stream_groq_response(
    messages,
    temperature=0.7,
    max_completion_tokens=1024,
    top_p=0.9,
    # top_k=40
)
print("Time taken: ", time.time()-s5)

# Example 6: Maximum diversity (high temperature, high top_p, high top_k)
print("\n=== Example 6: Maximum Diversity ===")
s6 = time.time()
response = make_groq_request(
    messages,
    temperature=2.0,
    max_completion_tokens=1024,
    top_p=1.0,
    # top_k=100
)
print(json.dumps(response, indent=2))
print("Time taken: ", time.time()-s6)
print("Total time taken: ", time.time()-s1)
