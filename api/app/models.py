from sqlmodel import Field, SQLModel
from datetime import datetime

class Company(SQLModel, table=True):
   company_id: int = Field(primary_key=True)
   name: str
   activity_type: str
   count_of_workers: int

class Product(SQLModel, table=True):
   product_id: int = Field(primary_key=True)
   valid_until: datetime
   fullName: str
   price: int

class Deliveries(SQLModel, table=True):
   delivery_id: int = Field(primary_key=True)
   company_id: int
   product_id: int
   date: datetime
   size: int
   price: int
