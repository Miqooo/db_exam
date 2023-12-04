from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime

from pydantic import BaseModel

class Company(SQLModel, table=True):
   company_id: int = Field(primary_key=True)
   name: str
   activity_type: str
   count_of_workers: int

class Product(SQLModel, table=True):
   product_id: int = Field(primary_key=True)
   product_name: str
   valid_until: Optional[datetime]
   measurement: str
   price: int

class Supplies(SQLModel, table=True):
   supply_id: int = Field(primary_key=True)
   company_id: int
   product_id: int
   date: Optional[datetime]
   size: int
   price: int
