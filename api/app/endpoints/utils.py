
from json.decoder import JSONDecodeError
from pydantic import BaseModel
from typing import Any

from fastapi import HTTPException, Request
from fastapi.encoders import jsonable_encoder

class ResponseModel(BaseModel):
    error: bool
    message: Any
    code: int

def ResponseWrapper(error: bool, message: Any, code: int = 200) -> ResponseModel:
    response = ResponseModel(error=error, message=message, code=code)
    if error:
        raise HTTPException(status_code=code, detail=response.dict())
    else:
        return response

async def validate_request(request: Request) -> None:
    content_type = request.headers.get('Content-Type')

    if content_type is None:
        ResponseWrapper(error=True, message="No Content-Type provided", code=500)
    else:
        try:
            return
        except JSONDecodeError:
            ResponseWrapper(error=True, message="Invalid JSON data", code=400)
    # else:
    #     ResponseWrapper(error=True, message="Content-Type not supported", code=415)


# @router.post("/company")
# async def add_company(request: Request):
#     content_type = request.headers.get('Content-Type')
    
#     if content_type is None:
#         HTTPException(status_code=500, detail=f"No Content-Type provided")
#     elif content_type == 'application/json':
#         try:
#             json = await request.json()
#             return json
#         except JSONDecodeError:
#             HTTPException(status_code=400, detail=f"Invalid JSON data")
#     else:
#         HTTPException(status_code=415, detail=f"Content-Type not supported")
