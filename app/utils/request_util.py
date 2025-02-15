from fastapi import Request, Depends



def get_request(request: Request):
    return request

class RequestContext:
    def __init__(self, request: Request):
        self.request = request

# Dependency to create a RequestContext instance
def get_request_context(request: Request = Depends(get_request)):
    return RequestContext(request)