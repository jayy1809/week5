from fastapi import Depends, Request
from app.services.request_services import RequestService



class RequestUseCases:
    def __init__(self,request_service: RequestService = Depends()):
        self.request_service = request_service

    async def get_request(self):
        return await self.request_service.do_something_with_request()
    
    async def example_route(self, request: Request):
        return await self.request_service.example_route(request)