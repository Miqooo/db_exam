import requests
import json


api_host = "http://localhost:5001"

def print_delimiter():
    print("\n" + "=" * 50)

def print_success_or_error(response_json):
    if ("error" not in response_json or response_json["error"] == True) and "results" not in response_json:
        print("❌ Error in response:")

    else:
        print("✅ Success! Response:")

def GET(host, endpoint, query_params):
    url = host + endpoint
    response = requests.get(url, params=query_params)
    response_json = json.loads(response.text)
    
    if ("error" not in response_json or response_json["error"] == True) and "results" not in response_json:
        print("url: ", url, "\n", query_params)

    return response_json

def POST(host, endpoint, data):
    url = host + endpoint
    response = requests.post(url, json = data)
    response_json = json.loads(response.text)

    if ("error" not in response_json or response_json["error"] == True) and "results" not in response_json:
        print("url: ", url, "\n", data)

    return response_json 
    
def PUT(host, endpoint, data):
    url = host + endpoint
    response = requests.put(url, json = data)
    response_json = json.loads(response.text)

    if ("error" not in response_json or response_json["error"] == True) and "results" not in response_json:
        print("url: ", url, "\n", data)

    return response_json
        
def DELET(host, endpoint, data = None):
    url = host + endpoint
    response = requests.delete(url, json = data)
    response_json = json.loads(response.text)

    if ("error" not in response_json or response_json["error"] == True) and "results" not in response_json:
        print("url: ", url, "\n", data)

    return response_json