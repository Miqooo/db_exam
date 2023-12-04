from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.responses import JSONResponse

from typing import List, Dict, Any

from sqlmodel import Session
from sqlmodel import select

from ..models import *
from ..init import engine
from .utils import *

router = APIRouter()

@router.get("/companies/", response_model=ResponseModel)
async def get_companies():
    with Session(engine) as session:
        companies = session.exec(select(Company)).all()
        return ResponseWrapper(error=False, message=companies)

@router.post("/company", response_model=ResponseModel)
async def add_company(request: Request, name: str = Form(...), activity_type: str = Form(...), count_of_workers: int = Form(...)):
    try:
        await validate_request(request)
        
        with Session(engine) as session:
            company = Company(name=name, activity_type=activity_type, count_of_workers=count_of_workers)
            session.add(company)
            session.commit()
            session.refresh(company)
    
            return ResponseWrapper(error=False, message="success")
    
    except HTTPException as exc:
       return ResponseWrapper(error=True, message=JSONResponse(content=exc.detail, status_code=exc.status_code), code=400)
