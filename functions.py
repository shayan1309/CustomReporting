# functions/api.py

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def API_auth(api_key):
    # Your API authentication code here
    # Replace "YOUR_API_KEY_HERE" with your actual API key
    api_key_header = {
        "Authorization": api_key
    }

    # Make an API request and return the response
    api_url = "https://v1serv-prod.evidencepartners.com/api/v1/auth/"
    response = requests.post(api_url, headers=api_key_header)

    if response.status_code == 200:
        return json.loads(response.text)["token"]
    else:
        return None


def Get_projectIDbyname(auth_token, project_name):
    # Your code for getting project ID here
    url = "https://v1serv-prod.evidencepartners.com/api/v1/projects"
    bearer_token = "Bearer " + auth_token
    payload = {}
    headers = {
        'Authorization': bearer_token
    }

    fullresponse = requests.request("GET", url, headers=headers, data=payload)
    response = json.loads(fullresponse.text)
    for project in response:
        if project["name"] == project_name:
            projectid = project["id"]
            break
    return projectid
    pass


# Define other API-related functions

def Get_allprojectRefIDs(auth_token, project_id):
    # Function to return project ID from given project name
    #url = "https://v1serv-prod.evidencepartners.com/api/v1/projects/:project_id/references?page_size=<int>&page=<int>"
    url = "https://v1serv-prod.evidencepartners.com/api/v1/projects/" + str(project_id) + "/references?page_size=100&page=1"
    bearer_token = "Bearer "+auth_token
    payload = {}
    headers = {
        'Authorization': bearer_token
    }

    fullresponse = requests.request("GET", url, headers=headers, data=payload)
    response = json.loads(fullresponse.text)
    return response

def Get_savedreportbyname(auth_token, project_id, saved_report):
    # Function to return project ID from given project name
    url = "https://v1serv-prod.evidencepartners.com/api/v1/datarama/savedreports?project_id="+str(project_id)
    bearer_token = "Bearer "+auth_token
    payload = {}
    headers = {
        'Authorization': bearer_token
    }

    fullresponse = requests.request("GET", url, headers=headers, data=payload)
    response = json.loads(fullresponse.text)
    for report in response:
        if report["name"] == saved_report:
            reportid = report["id"]
            break
    return reportid

def API_rundataramareport(auth_token, project_id, savedreport_id):
    # Function to return project ID from given project name
    url = "https://v1serv-prod.evidencepartners.com/api/v1/datarama/query"
    bearer_token = "Bearer "+auth_token
    payload_string = "{\"project_id\": " + str(project_id) + ", \"saved_report_id\": " + str(savedreport_id) + ", \"use_saved_format\": true}"
    #payload_string = "{\"project_id\": " + str(project_id) + ", \"saved_report_id\": " + str(savedreport_id) + "}"
    payload = payload_string
    headers = {
        'Content-Type': 'application/json',
        'Authorization': bearer_token
    }

    fullresponse = requests.request("POST", url, headers=headers, data=payload)
    #response = json.loads(fullresponse.text)
    response = fullresponse.content
    return response

def handler(request):
    # Handle incoming requests to this function
    data = request.get_json()

    api_key = data["api_key"]
    project_name = data["project_name"]
    saved_report_name = data["saved_report_name"]
    file_path = data["file_path"]

    # Authenticate and get an API token
    auth_token = API_auth(api_key)

    if auth_token is not None:
        # Call other API-related functions as needed
        # project_id = Get_projectIDbyname(auth_token, project_name)
        # ...
        return jsonify({"status": "success", "message": "API call succeeded."})
    else:
        return jsonify({"status": "error", "message": "API authentication failed."})
