from sqlmodel import Session, create_engine
from faker import Faker

from .models import *

DATABASE_URL = 'postgresql://postgres:postgres@db:5432/db'
# conn = psycopg2.connect("dbname='db' user='postgres' host='db' password='postgres'")

engine = create_engine(DATABASE_URL)
faker = Faker()

def initDatabase():
    SQLModel.metadata.create_all(engine)
    fillDatabase()

def fillDatabase(companies_count = 5, products_count=5, deliveries_count=7):
    with Session(engine) as session:
        for _ in range(companies_count):
            name = faker.name()
            activity_type = faker.word()
            count_of_workers = faker.random_int(min=5, max=15)
            company = Company(name=name, activity_type=activity_type, count_of_workers=count_of_workers)
            session.add(company)
        session.commit()


        measurments = ["kg", "g", "unit", "chunk"]
        for _ in range(products_count):
            fullName = faker.name()
            valid_until = faker.date()
            measurment = faker.rando_elements(measurments)
            price = faker.random_int(min=5, max=15)
            product = Product(fullName = fullName, valid_until=valid_until, measurment=measurment, price=price)
            session.add(product)
        session.commit()


        for company_id in range(1, companies_count+1):
            elements = list(range(1, products_count+1))
            product_ids = faker.random_elements(elements=elements, length=faker.random_int(min=5, max=8))

            for product_id in product_ids:
                date = faker.date()
                size = faker.random_int(min=10, max=100)
                price = faker.random_int(min=2, max=10)

                delivery = Deliveries(company_id = company_id, product_id=product_id, date=date, size=size, price=price)
                session.add(delivery)
        session.commit()