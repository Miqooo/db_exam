from fastapi import APIRouter, HTTPException, Request, Form, Query
from fastapi.responses import JSONResponse

from typing import List, Dict, Any

from sqlmodel import Session, select

from ..models import *
from ..init import engine
from .utils import *

supplyRouter = APIRouter()

# GET 

@supplyRouter.get("/supplies/", response_model=PaginationModel)
async def get_supplies(limit: int = Query(10, gt=0), 
                        page: int = Query(1, gt=0),
                        minPrice: int = Query(0, gt=0)):
    with Session(engine) as session:
        query = select(Supplies).where(Supplies.price >= minPrice)
        results = session.exec(query).all()
        return PaginationWrapper(results=results, limit=limit, page=page)


# POST

@supplyRouter.post("/supply", response_model=ResponseModel)
async def add_company(supply: SuppliesModel):
    try:
        # await validate_request(request)
        
        with Session(engine) as session:
            supply = Supplies(company_id=supply.company_id, 
                              product_id=supply.product_id, 
                              date=supply.date,
                              size=supply.size,
                              price=supply.price)

            session.add(supply)
            session.commit()
            session.refresh(supply)
    
            return ResponseModel(error=False, message="success")
    
    except HTTPException as exc:
       return ResponseModel(error=True, message=JSONResponse(content=exc.detail, status_code=exc.status_code), code=400)