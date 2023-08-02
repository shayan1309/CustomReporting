import pandas as pd
import os
import requests
import json
import csv
import time
from datetime import datetime
from io import StringIO
import pandas as pd
from docxtpl import DocxTemplate

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

# Main
file_dir = "C:\Python/"
credentials = "Key da4f8fc9edc769e3fd235a412d892b37"
projectname = "My Report"
Auth_key = API_auth(credentials)
print (Auth_key)
projectid = Get_projectIDbyname(Auth_key, projectname)
print (projectid)
allrefid = Get_allprojectRefIDs(Auth_key, projectid)
savedreportid = Get_savedreportbyname(Auth_key, projectid, "Study Details")
print(savedreportid)
report_data = API_rundataramareport(Auth_key, projectid, savedreportid)
report_data = report_data.decode("utf-8")
print(report_data)
io_report_data = StringIO(report_data)
df = pd.read_csv(io_report_data)
print(df)


#df = pd.read_csv("Client-Data-SingleData.csv")
# newdf =df.dropna()
doc = DocxTemplate("C:\Python\\MyReportTemplate.docx")
#"C:\\Python\\Custom Tag Reporting\\Derektemplate.docx"
data = []
rid = set()
for index,row in df.iterrows():
    data_for_rows = {}
    rid.add(row['Refid'])
    for col in df.columns:
        if not pd.isna(row[col]):
         data_for_rows[col] = row[col]
    data.append(data_for_rows)
# print(rid)
context = {
    'riddata': rid,
    'rowdata': data
}
print(context)
doc.render(context)
doc.save("C:\\Python\\Client_Report_Single_Data.docx")

#flat.to_csv('TestOutput.csv')
 #C:\Python\Custom Tag Reporting\Template
 #Derektemplate.docx