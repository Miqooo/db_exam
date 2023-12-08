import requests
import json
import csv
import os

import argparse

from faker import Faker
from api_service import *

faker = Faker()

host = "http://0.0.0.0:5001/"

def fillDatabase(companies_count = 7, products_count=50, supplies_count=6):
    companies = readDataList("resources", "companies.csv")
    activityList = readDataList("resources", "activity_types.csv")
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
        

    measurements = readDataList("resources", "measurements.csv")
    productList = readDataList("resources", "products.csv")
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


def readDataList(dir, filename):
    file_path = os.path.join(os.path.dirname(__file__), dir, filename)

    data = []
    with open(file_path, mode="r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            name = row.get('name')
            if name:
                data.append(name)

    return data


def main():
    parser = argparse.ArgumentParser(description="API utility.")
    
    subparsers = parser.add_subparsers(dest='command')
    
    fill_parser = subparsers.add_parser('fill', help='Fill the database with random data')
    
    post_parser = subparsers.add_parser('post', help='Make a POST request to a specified endpoint')
    post_parser.add_argument('-e', '--endpoint', type=str, required=True, help='API endpoint for the POST request')
    post_parser.add_argument('data', type=json.loads, help='JSON data to POST to the endpoint')
    
    # Sub-parser for GET requests
    get_parser = subparsers.add_parser('get', help='Make a GET request to a specified endpoint')
    get_parser.add_argument('-e', '--endpoint', type=str, required=True, help='API endpoint for the GET request')
    get_parser.add_argument('-p', '--params', nargs='*', type=json.loads, default=[], help='Query parameters as an array of JSON strings')
    
    args = parser.parse_args()

    if args.command == 'fill':
        fillDatabase()
    elif args.command == 'post':
        POST(host=host, endpoint=args.endpoint, data=args.data)
    elif args.command == 'get':
        GET(host=host, endpoint=args.endpoint, params=args.params)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
