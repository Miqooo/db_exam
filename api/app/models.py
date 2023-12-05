from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel

class CompanyModel(BaseModel):
   name: str
   activity_type: str = Field("Finance")
   count_of_workers: int = Field(1)

class Company(SQLModel, table=True):
   company_id: int = Field(primary_key=True)
   name: str
   activity_type: str
   count_of_workers: int


class ProductModel(BaseModel):
   product_name: str
   valid_until: Optional[datetime] = Field(default=None)
   measurement: str = Field("piece")
   price: int = Field(0)

class Product(SQLModel, table=True):
   product_id: int = Field(primary_key=True)
   product_name: str
   valid_until: Optional[datetime]
   measurement: str
   price: int

class SuppliesModel(BaseModel):
   company_id: int
   product_id: int
   date: Optional[datetime]
   size: int = Field(default=1)
   price: int = Field(default=0)

class Supplies(SQLModel, table=True):
   supply_id: int = Field(primary_key=True)
   company_id: int = Field(foreign_key="company.company_id")
   product_id: int = Field(foreign_key="product.product_id")
   date: Optional[datetime]
   size: int
   price: int

   product: Optional[List[Product]] = Relationship()
   company: Optional[List[Company]] = Relationship()



