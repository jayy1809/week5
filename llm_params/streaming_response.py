from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import httpx
import json
import asyncio
from typing import Dict, List, Any
from pydantic import BaseModel
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")  
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    temperature: float = 0.7
    max_completion_tokens: int = 1024
    top_p: float = 0.9
    stream: bool = True


async def stream_groq_response(data: Dict[str, Any]):
    """
    Generator function to stream Groq API responses
    """
    async with httpx.AsyncClient() as client:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        try:
            async with client.stream(
                "POST",
                GROQ_API_URL,
                headers=headers,
                json=data,
                timeout=30.0
            ) as response:
                response.raise_for_status()
                
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        try:
                            # Remove "data: " prefix and parse JSON
                            json_data = json.loads(line[6:])
                            print(f"json: {json_data}")
                            
                            # Extract content from the response
                            if json_data.get("choices"):
                                content = json_data["choices"][0].get("delta", {}).get("content", "")
                                if content:
                                    # Yield content in SSE format
                                    yield f"data: {json.dumps({'content': content})}\n\n"
                        except json.JSONDecodeError:
                            continue
                    
                # Send end marker
                yield "data: [DONE]\n\n"
                
        except httpx.HTTPError as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

@app.post("/chat/stream")
async def stream_chat(request: ChatRequest):
    """
    Endpoint to stream chat completions from Groq
    """
    # Prepare the request data for Groq
    groq_request = {
        "messages": [{"role": msg.role, "content": msg.content} for msg in request.messages],
        "model": "llama-3.3-70b-versatile",
        "temperature": request.temperature,
        "max_completion_tokens": request.max_completion_tokens,
        "top_p": request.top_p,
        "stream": request.stream,
    }
    
    if request.stop:
        groq_request["stop"] = request.stop

    return StreamingResponse(
        stream_groq_response(groq_request),
        media_type="text/event-stream"
    )

# Example usage endpoint
@app.post("/chat/example")
async def example_chat():
    """
    Example endpoint with predefined messages
    """
    example_request = ChatRequest(
        messages=[
            Message(role="system", content="You are a helpful assistant."),
            Message(role="user", content="Tell me a short story about space exploration.")
        ],
        temperature=0.8,
        max_completion_tokens=1024,
        top_p=0.95,
        stream=True
    )
    
    return StreamingResponse(
        stream_groq_response({
            "messages": [{"role": msg.role, "content": msg.content} for msg in example_request.messages],
            "model": "llama-3.3-70b-versatile",
            "temperature": example_request.temperature,
            "max_completion_tokens": example_request.max_completion_tokens,
            "top_p": example_request.top_p,
            "stream": example_request.stream
        }),
        media_type="text/event-stream"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)