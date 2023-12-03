from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException

from sqlalchemy import func, and_
from sqlmodel import Session
from sqlmodel import select

from .models import *
from .init import *

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    print("Running startup code")
    initDatabase()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/companies/")
async def get_companies():
    with Session(engine) as session:
        companies = session.exec(
            select(Company)
        )
        
        if not companies:
            raise HTTPException(status_code=404, detail="Companies not found")

        return companies
    
# @app.get("/products/")
# async def get_products():
#     with Session(engine) as session:
#         products = session.exec(
#             select(Product).where()
#         )
#         if not products:
#             raise HTTPException(status_code=404, detail="Products not found")
#         return products


# @app.get("/deliveries/")
# async def get_deliveries():
#     with Session(engine) as session:
#         deliveries = session.exec(
#             select(Deliveries).where()
#         )
#         if not deliveries:
#             raise HTTPException(status_code=404, detail="Deliveries not found")

#         return deliveries