from fastapi import APIRouter, FastAPI
from .endpoints.companies import router

from .models import *
from .init import *

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    print("Running startup code")
    initDatabase()
    fillDatabase()

@app.get("/")
async def root():
    return {"message": "Hello World"}

