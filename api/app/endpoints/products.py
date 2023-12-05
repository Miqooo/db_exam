from fastapi import APIRouter, HTTPException, Request, Form, Query
from fastapi.responses import JSONResponse

from typing import List, Dict, Any

from sqlmodel import Session, select

from ..models import *
from ..init import engine
from .utils import *

productRouter = APIRouter()

# GET 

@productRouter.get("/products/", response_model=PaginationModel)
async def get_products(limit: int = Query(10, gt=0), page: int = Query(1, gt=0)):
    with Session(engine) as session:
        results = session.exec(select(Product)).all()
        return PaginationWrapper(results=results, limit=limit, page=page)


# POST 

@productRouter.post("/product", response_model=ResponseModel)
async def add_product(product: ProductModel):
    try:
        # await validate_request(request)
        
        with Session(engine) as session:
            product = Product(product_name=product.product_name, price=product.price, measurement=product.measurement, valid_until=product.valid_until)
            
            session.add(product)
            session.commit()
            session.refresh(product)
    
        return ResponseModel(error=False, message="success")
    
    except HTTPException as exc:
       return ResponseModel(error=True, message=JSONResponse(content=exc.detail, status_code=exc.status_code), code=400)
