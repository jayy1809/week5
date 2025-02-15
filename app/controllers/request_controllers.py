from fastapi import Depends, Request
from app.usecases.request_usecases import RequestUseCases

class RequestController:
    def __init__(self,request_usecases: RequestUseCases = Depends(RequestUseCases)):
        self.request_usecases = request_usecases
    
    async def get_request(self):
        return await self.request_usecases.get_request()
    
    async def example_route(self, request: Request):
        return await self.request_usecases.example_route(request)