from fastapi import APIRouter, HTTPException, Request, Form, Query
from fastapi.responses import JSONResponse

from typing import List, Dict, Any

from sqlmodel import Session
from sqlmodel import select

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
        return pagination_wrapper(results=results, limit=limit, page=page)


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
    

# UPDATE

@supplyRouter.put("/supply/update/{supply_id}", response_model=ResponseModel)
def update_supplies(supply_id: int, supply: SuppliesModel):
    with Session(engine) as session:
        query = select(Supplies).where(Supplies.supply_id == supply_id)
        result = session.exec(query).first()
        
        if result is None:
            return ResponseModel(error=True, message="supply_id not found", code=400)
        
        for key, value in supply.dict().items():
            setattr(result, key, value)
        
        session.commit()
        session.refresh(result)
        return ResponseModel(error=False, message="updated")