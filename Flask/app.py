# app.py
"""
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

"""

from flask import Flask, flash, render_template, request
from HelixLoad import initiateHelixLoad as initiateHelixLoad


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        Source = request.form['Source']
        LoadType = request.form['LoadType']
        if Source =="Helix" and LoadType !="" :
            initiateHelixLoad(LoadType)
            userMsg = f"Hello, {Source} data load into AI Model is Completed now!"
            #flash(userMsg, category='success')
            return render_template('index.html', greeting = userMsg)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


