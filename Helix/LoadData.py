import configs
import requests
import Auth
from Programs.SQL_Functions import create_connection as dbconnection
from Programs.SQL_Functions import create_record as insertrecord


 #Get Helix Token
helixToken= Auth.GetAuthToken()

 #use token in GET method
GetIncidentsUrl= configs.BaseUrl+configs.IncidentsUrl+configs.QueryQual+configs.IncidentFieldList
print(GetIncidentsUrl)
print("\n")
HttpHeaders = {
    'Authorization': helixToken
 }
HttpResponse = requests.get(GetIncidentsUrl, headers=HttpHeaders)
response_data=HttpResponse.json()

conn = dbconnection()
counter = 0
for entry in response_data['entries']:
    values = entry['values']
    incident_id = values['Incident Number']
    incident_status = values['Status']
    incident_summary = values['Description']
    data = (incident_status, incident_summary,incident_id)
    print(data)
 # Insert records in Databse table
    insertrecord(conn, data)

#close database connection
conn.close()    