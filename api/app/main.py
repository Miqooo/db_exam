from fastapi import APIRouter, FastAPI
from .endpoints.companies import companyRouter
from .endpoints.products import productRouter
from .endpoints.sipplies import supplyRouter

from .models import *
from .init import *

app = FastAPI()
app.include_router(productRouter)
app.include_router(companyRouter)
app.include_router(supplyRouter)

@app.on_event("startup")
async def startup_event():
    print("Running startup code")
    initDatabase()
    # fillDatabase()

@app.get("/")
async def root():
    return {"message": "Hello World"}

