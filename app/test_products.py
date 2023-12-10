import json
import requests

from api_service import *

def run():
    # Test GET request for products
    print_delimiter()
    print("Testing GET request for products")
    response_get_products = GET(api_host, "/products/", query_params={"order_by": "product_id", "asc": True, "limit": 10, "page": 1})
    print_success_or_error(response_get_products)
    print(json.dumps(response_get_products, indent=4))

    # Test GET request for a specific product
    print_delimiter()
    print("Testing GET request for a specific product")
    product_id_to_get = 1
    response_get_product = GET(api_host, f"/product/{product_id_to_get}", query_params={})
    print_success_or_error(response_get_product)
    print(json.dumps(response_get_product, indent=4))

    # Test POST request to add a new product
    print_delimiter()
    print("Testing POST request to add a new product")
    product_data_to_post = {
        "product_name": "TestProduct",
        "price": 20.0,
        "measurement": "units",
        "valid_until": "2023-12-31T00:00:00"
    }
    response_post_product = POST(api_host, "/product", data=product_data_to_post)
    print_success_or_error(response_post_product)
    print(json.dumps(response_post_product, indent=4))

    # Test DELETE request for a product
    print_delimiter()
    print("Testing DELETE request for a product")
    product_id_to_delete = 2
    response_delete_product = DELET(api_host, f"/product/{product_id_to_delete}")
    print_success_or_error(response_delete_product)
    print(json.dumps(response_delete_product, indent=4))
