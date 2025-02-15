from fastapi import Request, Depends, HTTPException
from app.middlewares.context import request_context
import asyncio

import logging

# Configure logging to write to a file
logging.basicConfig(
    filename="app2.log",  # Log file name
    level=logging.INFO,  # Log level
    format="%(asctime)s - %(message)s",  # Log format
)



class RequestService:
    def __init__(self):
        pass

    async def do_something_with_request(self):
        try:
            request = request_context.get()
            if request is None :
                raise Exception("Request is None")
            await asyncio.sleep(2)
            request_json = await request.json()
            # print(request.client.host)\
            return {
                "hello": "world, from service",
                "request_json": f"{dict(request)}"
            }
        except Exception as e:
            return {
                "error": str(e)
            }
    
    async def example_route(self, request: Request):
        try:
            await asyncio.sleep(2)
            request2 = request_context.get()
            if request.state.newid == request2.state.newid:
                logging.info("ALLLLLLLLLLL IZZZZZZZ WELLLLLLLLL!!")

            else:
                logging.error("User: Request context mismatch detected!")
                raise HTTPException(status_code=500, detail="Request context mismatch detected!")


            # if request != request2:
            #     raise HTTPException(status_code=500, detail="Request context mismatch detected!")
            # if request2 is None:
            #     raise Exception("Request2 is None")
        
            await asyncio.sleep(2)
            return {
                "message": "request got till service",
                "request_json": f"{dict(request2)}"
            }
        except Exception as e:
            return {
                "error": str(e)
            }
                