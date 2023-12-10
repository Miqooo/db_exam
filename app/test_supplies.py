import json
import requests

from api_service import *

def run():
    print_delimiter()
    print("Testing GET request for supplies")
    response_get_supplies = GET(api_host, "/supplies/", query_params={"limit": 10, "page": 1, "minPrice": 10})
    print_success_or_error(response_get_supplies)
    print(json.dumps(response_get_supplies, indent=4))

    # Test POST request to add a new supply
    print_delimiter()
    print("Testing POST request to add a new supply")
    supply_data_to_post = {
        "company_id": 1,
        "product_id": 1,
        "date": "2023-12-10T00:00:01",
        "size": 5,
        "price": 15.0
    }
    response_post_supply = POST(api_host, "/supply", data=supply_data_to_post)
    print_success_or_error(response_post_supply)
    print(json.dumps(response_post_supply, indent=4))

    # Test PUT request to update a supply
    print_delimiter()
    print("Testing PUT request to update a supply")
    supply_id_to_update = 8
    supply_data_to_update = {
        "company_id": 1,
        "product_id": 1,
        "size": 8,
        "price": -20.0
    }
    response_put_supply = PUT(api_host, f"/supply/update/{supply_id_to_update}", data=supply_data_to_update)
    print_success_or_error(response_put_supply)
    print(json.dumps(response_put_supply, indent=4))