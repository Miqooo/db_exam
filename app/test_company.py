import json
import requests

from api_service import *

def run():
    print_delimiter()
    print("Testing GET request for company")
    response_get = GET(api_host, "/company/1", query_params={})
    print_success_or_error(response_get)
    print(json.dumps(response_get, indent=4))

    # Test SORT request
    print_delimiter()
    print("Testing SORT request for companies")
    response_sort = GET(api_host, "/companies/", query_params={"order_by": "company_id", "asc": True, "limit": 10, "page": 1})
    print_success_or_error(response_sort)
    print(json.dumps(response_sort, indent=4))

    # Test SELECT ... WHERE, JOIN, GROUP BY request
    print_delimiter()
    print("Testing SELECT ... WHERE, JOIN, GROUP BY request for total")
    response_total = GET(api_host, "/companies/total", query_params={"limit": 10, "page": 1})
    print_success_or_error(response_total)
    print(json.dumps(response_total, indent=4))

    # Test POST request
    print_delimiter()
    print("Testing POST request to add a new company")
    company_data_to_post = {"name": "TestCompany", "activity_type": "TestActivity", "count_of_workers": 50}
    response_post = POST(api_host, "/company", data=company_data_to_post)
    print_success_or_error(response_post)
    print(json.dumps(response_post, indent=4))

    # Test DELETE request
    print_delimiter()
    print("Testing DELETE request for a company")
    response_delete = DELET(api_host, "/company/2")
    print_success_or_error(response_delete)
    print(json.dumps(response_delete, indent=4))