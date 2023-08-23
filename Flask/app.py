# app.py
import requests
from Auth import GetAuthToken as Auth
from configs import GetIncDataUrl as IncidentsUrl
from SQL_Functions import create_connection as dbconnection
from SQL_Functions import create_record as insertrecord
from flask import Flask, request, jsonify

app = Flask(__name__)

# @app.get("/records")
# def get_countries():
    #return jsonify(countries)

@app.post("/load")
def loadDataFromHelix():
    if request.is_json:
        payload = request.get_json()
        source = payload["source"]
        counter = 0        
        if source == "Helix":
             #Get Helix Token
            helixToken= Auth()
            
            HttpHeaders = {
                        'Authorization': helixToken
                         }
            #Get Call to Helix to retrieve Records
            HttpResponse = requests.get(IncidentsUrl, headers=HttpHeaders)
            response_data=HttpResponse.json()

            conn = dbconnection()
            
            for entry in response_data['entries']:
                    values = entry['values']
                    incident_id = values['Incident Number']
                    incident_status = values['Status']
                    incident_summary = values['Description']
                    data = (incident_status, incident_summary,incident_id)
                    print(data)
                    # Insert records in Databse table
                    insertrecord(conn, data)
                    counter = counter + 1
                    #close database connection
            conn.close()
            return {"Status" : "Success", "Records Loaded" : str(counter)} , 200
        
    return {"error": "Request must be JSON"}, 415  