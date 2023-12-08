from fastapi import APIRouter, HTTPException, Request, Form, Query
from fastapi.responses import JSONResponse

from typing import List, Dict, Any

from sqlmodel import Session, select, desc
from sqlalchemy import func

from ..models import *
from ..init import engine
from .utils import *

companyRouter = APIRouter()

# GET
@companyRouter.get("/companies/", response_model=PaginationModel)
async def get_companies(limit: int = Query(10, gt=0), page: int = Query(1, gt=0)):
    with Session(engine) as session:
        results = session.exec(select(Company)).all()
        return PaginationWrapper(results=results, limit=limit, page=page)

@companyRouter.get("/companies/total", response_model=PaginationModel)
async def get_companies(limit: int = Query(10, gt=0), page: int = Query(1, gt=0)):
    with Session(engine) as session:
        query = (
        select(
            Company.name.label("company_name"),
            func.array_agg(Product.product_name).label("all_products"),
            func.sum(Supplies.size * Supplies.price).label('total_sales_amount')
        )
        .join(Supplies, Company.company_id == Supplies.company_id)
        .join(Product, Supplies.product_id == Product.product_id)
        .group_by(Company.name)
    )

    results = session.exec(query).all()
    result_dicts = [
            {
                'company_name': result[0],
                'product_name': result[1],
                'total_sales_amount': result[2],
            }
            for result in results
        ]
    
    return PaginationWrapper(results=result_dicts, limit=limit, page=page)

# POST
@companyRouter.post("/company", response_model=ResponseModel)
async def add_company(company: CompanyModel):
    try:
        with Session(engine) as session:
            company = Company(name=company.name, 
                              activity_type=company.activity_type, 
                              count_of_workers=company.count_of_workers)

            session.add(company)
            session.commit()
            session.refresh(company)
    
            return ResponseModel(error=False, message="success")
    
    except HTTPException as exc:
       return ResponseModel(error=True, message=JSONResponse(content=exc.detail, status_code=exc.status_code), code=400)
