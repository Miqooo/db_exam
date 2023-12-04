# from fastapi import APIRouter

# from typing import List, Optional
# from sqlmodel import Session
# from sqlmodel import select

# from ..init import engine
# from ..models import *

# router = APIRouter()

# @router.get("/products/", response_model=List[Product])
# async def get_companies():
#     with Session(engine) as session:
#         products = session.exec(select(Product)).all()
#         return products
    
# @router.get("/supplies/", response_model=List[Supplies])
# async def get_companies():
#     with Session(engine) as session:
#         supplies = session.exec(select(Supplies)).all()
#         return supplies
    