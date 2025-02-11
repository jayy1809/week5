import httpx
import json
import asyncio
import time
import os
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")  
BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

async def make_groq_request_async(messages: list, **params) -> Dict[Any, Any]:
    """
    Make an asynchronous request to Groq API with specified parameters
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
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(BASE_URL, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return None

async def main():
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a short story about a magical forest."}
    ]
    
    start_time = time.time()
    responses = await asyncio.gather(
        make_groq_request_async(messages, temperature=0.7, max_completion_tokens=1024, top_p=0.9),
        make_groq_request_async(messages, temperature=1.5, max_completion_tokens=1024, top_p=0.9),
        make_groq_request_async(messages, temperature=0.7, max_completion_tokens=1024, stop=[".", "!", "?"], top_p=0.9),
        make_groq_request_async(messages, temperature=0.3, max_completion_tokens=1024, top_p=0.5),
        make_groq_request_async(messages, temperature=2.0, max_completion_tokens=1024, top_p=1.0)
    )
    
    for idx, response in enumerate(responses, start=1):
        print(f"\n=== Example {idx} Response ===")
        print(json.dumps(response, indent=2))
    
    print("Total time taken:", time.time() - start_time)

if __name__ == "__main__":
    asyncio.run(main())
