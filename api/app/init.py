import os
import csv
from sqlmodel import Session, create_engine, select
from faker import Faker

from .models import *

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
faker = Faker()

def init_database():
    SQLModel.metadata.create_all(engine)
