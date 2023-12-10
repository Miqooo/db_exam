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
async def get_products(
    order_by: str = "product_id", 
    asc: bool = True,
    limit: int = Query(10, gt=0), 
    page: int = Query(1, gt=0)
):
    with Session(engine) as session:
        if not hasattr(Product, order_by):
            results = session.exec(select(Product)).all()
            return pagination_wrapper(results=results, limit=limit, page=page)

        if asc:
            results = session.exec(select(Product).order_by(getattr(Product, order_by))).all()
        else:
            results = session.exec(select(Product).order_by(getattr(Product, order_by).desc())).all()
        return pagination_wrapper(results=results, limit=limit, page=page)
    

@productRouter.get("/product/{product_id}", response_model=ResponseModel)
async def get_product(product_id: int):
    with Session(engine) as session:
        results = session.exec(select(Product).filter(Product.product_id == product_id)).first()
        if results is None:
            return ResponseModel(error=True, message="product_id not found", code=400)
        return ResponseModel(error=False, message=results)

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

# DELETE

@productRouter.delete("/product/{product_id}", response_model=ResponseModel)
def delete_product(product_id: int):
    with Session(engine) as session:
        supplies = session.exec(select(Supplies).filter(Supplies.product_id == product_id)).all()
        if len(supplies) != 0:
            for item in supplies:
                session.delete(item)
                session.commit()

        product = session.exec(select(Product).filter(Product.product_id == product_id)).first()
        if product is None:
            return ResponseModel(error=True, message="product_id not found", code=400)
        
        session.delete(product)
        session.commit()
        return ResponseModel(error=False, message="deleted")

