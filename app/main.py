import requests
import json
import csv
import os

import argparse
import test_company as test_company
import test_products as test_products
import test_supplies as test_supplies

from faker import Faker
from api_service import *


faker = Faker()

host = "http://localhost:5001/"

def fill_database(companies_count = 7, products_count=50, supplies_count=6):
    companies = read_data_list("resources", "companies.csv")
    activityList = read_data_list("resources", "activity_types.csv")
    for _ in range(companies_count):
        name = faker.random_element(companies)
        companies.remove(name)
        activity_type = faker.random_element(activityList)
        count_of_workers = faker.random_int(min=5, max=55)
        company = {
            "name": name,
            "activity_type": activity_type,
            "count_of_workers": count_of_workers 
        }
        POST(host=host, endpoint="company", data=company)
        

    measurements = read_data_list("resources", "measurements.csv")
    productList = read_data_list("resources", "products.csv")
    for _ in range(products_count):
        product_name = faker.random_element(productList)
        valid_until = faker.date_this_year(before_today=False, after_today=True)
        measurement = faker.random_element(measurements)
        price = faker.random_int(min=5, max=50)
        product = {
            "product_name": product_name,
            "valid_until": valid_until.strftime("%Y-%m-%dT%H:%M:%S"),
            "measurement": measurement,
            "price":price
        }
        POST(host=host, endpoint="product", data=product)

    for company_id in range(1, companies_count+1):
        elements = list(range(1, products_count+1))
        product_ids = faker.random_elements(elements=elements, length=faker.random_int(min=5, max=8))
        print(product_ids)
        
        for product_id in product_ids:
            date = faker.date_this_year(before_today=False, after_today=True)
            size = faker.random_int(min=10, max=100)
            price = faker.random_int(min=2, max=100)

            supply = {
                "company_id": company_id,
                "product_id": product_id,
                "date": date.strftime("%Y-%m-%dT%H:%M:%S"),
                "size": size,
                "price":price
            }
            POST(host=host, endpoint="supply", data=supply)

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

def test_GET():
    endpoint = "supply/1"
    params = {"limit": 100}
    GET(host=host, endpoint=endpoint, params=params)



def main():
    parser = argparse.ArgumentParser(description="API utility.")
    
    subparsers = parser.add_subparsers(dest='command')
    
    fill_parser = subparsers.add_parser('fill', help='Fill the database with random data')
    post_parser = subparsers.add_parser('company', help='')
    get_parser = subparsers.add_parser('product', help='')
    get_parser = subparsers.add_parser('supplies', help='')

    args = parser.parse_args()

    if args.command == 'fill':
        fill_database()
    elif args.command == 'company':
        test_company.run()

    elif args.command == 'product':
        test_products.run()

    elif args.command == 'supplies':
        test_supplies.run()
        pass

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
