import requests
import json

def POST(host, endpoint, data):
    url = host + endpoint
    response = requests.post(url, json = data)

    responseJson = json.loads(response.text)
    if "error" not in responseJson or responseJson["error"] == True:
        print("data: ", json.dumps(data, indent=4))
        print("response: ", json.dumps(responseJson, indent=4))
    else:
        print("success")
    

def GET(host, endpoint, queryParams):
    url = host + endpoint
    response = requests.get(url, params=queryParams)
    responseJson = json.loads(response.text)
    
    if "error" not in responseJson or responseJson["error"] == True:
        print("url: ", url, " | ", queryParams)
    
    print("response: ", json.dumps(responseJson, indent=4))
        