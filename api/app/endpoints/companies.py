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

@companyRouter.get("/company/{company_id}", response_model=ResponseModel)
async def get_company(company_id: int):
    with Session(engine) as session:
        results = session.exec(select(Company).filter(Company.company_id == company_id)).first()
        if results is None:
            return ResponseModel(error=True, message="company_id not found", code=404)
        return ResponseModel(error=False, message=results)

# SORT

@companyRouter.get("/companies/", response_model=PaginationModel)
async def get_products(
    order_by: str = "company_id", 
    asc: bool = True,
    limit: int = Query(10, gt=0), 
    page: int = Query(1, gt=0),
):
    with Session(engine) as session:
        if not hasattr(Company, order_by):
            results = session.exec(select(Company)).all()
            return pagination_wrapper(results=results, limit=limit, page=page)
        
        if asc:
            results = session.exec(select(Company).order_by(getattr(Company, order_by))).all()
        else:
            results = session.exec(select(Company).order_by(getattr(Company, order_by).desc())).all()

        return pagination_wrapper(results=results, limit=limit, page=page)
    
# SELECT ... WHERE
# JOIN
# GROUP BY

@companyRouter.get("/companies/total", response_model=PaginationModel)
async def get_total(limit: int = Query(10, gt=0), page: int = Query(1, gt=0)):
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
    
    return pagination_wrapper(results=result_dicts, limit=limit, page=page)


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
       return ResponseModel(error=True, message=JSONResponse(content=exc.detail, status_code=exc.status_code), code=exc.status_code)


# DELETE

@companyRouter.delete("/company/{company_id}", response_model=ResponseModel)
def delete_company(company_id: int):
    with Session(engine) as session:
        supplies = session.exec(select(Supplies).filter(Supplies.company_id == company_id)).all()
        if len(supplies) != 0:
            for item in supplies:
                session.delete(item)
                session.commit()

        company = session.exec(select(Company).filter(Company.company_id == company_id)).first()
        if company is None:
            return ResponseModel(error=True, message="company_id not found", code=404)
        
        session.delete(company)
        session.commit()
        return ResponseModel(error=False, message="deleted")
