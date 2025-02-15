from fastapi import Depends, APIRouter, Request
from app.controllers.request_controllers import RequestController
from app.utils.request_util import RequestContext, get_request_context
router = APIRouter()


@router.get("/request")
async def get_request(
    request_controller : RequestController = Depends()
):
    
    return await request_controller.get_request()


@router.post("/example")
async def example_route(
    request: Request,
    request_controller : RequestController = Depends()
):
    result = await request_controller.example_route(request)
    return {"message": "Request processed successfully", "data": result}



