from flask import Flask, render_template, request
import os
import requests
import json
from io import StringIO
import pandas as pd
from docxtpl import DocxTemplate

app = Flask(__name__)

def API_auth(encodedlogin):
    # Function to return  API Auth token
    url = "https://v1serv-prod.evidencepartners.com/api/v1/auth/"
    payload = {}
    headers = {
        'Authorization': encodedlogin
    }

    fullresponse = requests.request("POST", url, headers=headers, data=payload)
    response = json.loads(fullresponse.text)
    auth_key = response["token"]
    return auth_key


def Get_projectIDbyname(auth_token, project_name):
    # Function to return project ID from given project name
    url = "https://v1serv-prod.evidencepartners.com/api/v1/projects"
    bearer_token = "Bearer "+auth_token
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

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        api_key = request.form["api_key"]
        project_name = request.form["project_name"]
        saved_report_name = request.form["saved_report_name"]
        word_file = request.files["word_file"]

        # Save the uploaded file
        file_path = "C:\\Python\\uploads"
        word_file.save(os.path.join(file_path, word_file.filename))

        # Call your functions using the provided inputs
        Auth_key = API_auth(api_key)
        projectid = Get_projectIDbyname(Auth_key, project_name)
        savedreportid = Get_savedreportbyname(Auth_key, projectid, saved_report_name)
        report_data = API_rundataramareport(Auth_key, projectid, savedreportid)

        # Process report_data and saved word_file as needed
        # Your existing report generation and data processing logic here

        report_data = report_data.decode("utf-8")
        io_report_data = StringIO(report_data)
        df = pd.read_csv(io_report_data)  # Create DataFrame from report_data

        data = []
        rid = set()
        for index, row in df.iterrows():
            data_for_rows = {}
            rid.add(row['Refid'])
            for col in df.columns:
                if not pd.isna(row[col]):
                    data_for_rows[col] = row[col]
            data.append(data_for_rows)

        context = {
            'riddata': rid,
            'rowdata': data
        }
        print(context)

        doc = DocxTemplate("C:/Python/MyReportTemplate.docx")  # Update the correct path
        doc.render(context)
        doc.save("C:/Python/Client_Report_Single_Data.docx")  # Update the correct path

        return "Report generated successfully!"


    return render_template("index.html")

