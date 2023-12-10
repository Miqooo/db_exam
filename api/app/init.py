import os
import csv
from sqlmodel import Session, create_engine, select
from faker import Faker

from .models import *

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

print("URI: ", DATABASE_URL)
engine = create_engine(DATABASE_URL)

faker = Faker()

def init_database():
    SQLModel.metadata.create_all(engine)

def is_table_empty(table_model):
    with Session(engine) as session:
        result = session.exec(select(table_model)).first()
        return result is None


# def fill_database(companies_count = 15, products_count=25, supplies_count=10):
#     with Session(engine) as session:
#         if is_table_empty(Company):
#             companies= read_data_list("resources", "companies.csv")
#             activityList = read_data_list("resources", "activity_types.csv")
#             for _ in range(companies_count):

#                 name = faker.random_element(companies)
#                 companies.remove(name)

#                 activity_type = faker.random_element(activityList)
#                 count_of_workers = faker.random_int(min=5, max=55)

#                 company = Company(name=name, activity_type=activity_type, count_of_workers=count_of_workers)
#                 session.add(company)
#             session.commit()

#         if is_table_empty(Product):
#             measurements = read_data_list("resources", "measurements.csv")
#             productList = read_data_list("resources", "products.csv")
#             for _ in range(products_count):
#                 product_name = faker.random_element(productList)
#                 valid_until = faker.date_this_year(before_today=False, after_today=True)
#                 measurement = faker.random_element(measurements)
#                 price = faker.random_int(min=5, max=50)

#                 product = Product(product_name=product_name, valid_until=valid_until, measurement=measurement, price=price)
#                 session.add(product)
#             session.commit()

#         if is_table_empty(Supplies):
#             for company_id in range(1, companies_count+1):
#                 elements = list(range(1, products_count+1))
#                 product_ids = faker.random_elements(elements=elements, length=faker.random_int(min=5, max=8))

#                 for product_id in product_ids:
#                     date = faker.date_this_year(before_today=False, after_today=True)
#                     size = faker.random_int(min=10, max=100)
#                     price = faker.random_int(min=2, max=100)

#                     supply = Supplies(company_id = company_id, product_id=product_id, date=date, size=size, price=price)
#                     session.add(supply)
#             session.commit()

def read_data_list(dir, filename):
    file_path = os.path.join(os.path.dirname(__file__), dir, filename)

    data = []
    with open(file_path, mode="r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            name = row.get('name')
            if name:
                data.append(name)

    return data