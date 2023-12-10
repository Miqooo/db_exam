
from json.decoder import JSONDecodeError
from pydantic import BaseModel
from typing import Generic, List, Type, TypeVar, Optional

from fastapi import HTTPException, Request
from fastapi.encoders import jsonable_encoder

from sqlmodel import Field

T = TypeVar('T')

class ResponseModel(BaseModel, Generic[T]):
    error: bool = Field(default=False)
    message: T
    code: int = Field(default=200)

class PaginationModel(BaseModel, Generic[T]):
    limit: int
    page: int
    results: List[T]
    total: int

def pagination_wrapper(results, limit: int, page: int):
    total = len(results)
    start = (page - 1) * limit
    end = start + limit
    paginated_results = results[start:end]

    return PaginationModel[T](
        limit=limit,
        page=page,
        results=paginated_results,
        total=total
    )


async def validate_request(request: Request) -> None:
    content_type = request.headers.get('Content-Type')

    if content_type is None:
        ResponseModel(error=True, message="No Content-Type provided", code=500)
    else:
        try:
            return
        except JSONDecodeError:
            ResponseModel(error=True, message="Invalid JSON data", code=400)