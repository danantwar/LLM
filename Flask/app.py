# app.py
import requests
import configs as config
from Auth import GetAuthToken as Auth
from SQL_Functions import create_connection as dbconnection
from SQL_Functions import create_record as insertrecord
from flask import Flask, request, jsonify

#app = Flask(__name__)

#@app.get("/records")
#def get_countries():
    #return jsonify(countries)

#@app.post("/load")
#def loadDataFromHelix():
#if request.is_json:
#        payload = request.get_json()
#        source = payload["source"]
#        counter = 0        
#        if source == "Helix":
             #Get Helix Token

# Initialize DB Connection
conn = dbconnection()            
# Initialize Records Counter
counter = 0 

# Generate Helix Auth Token
helixToken= Auth()

# Prepare HTTP Headers for Helix Call
HttpHeaders = {
                'Authorization': helixToken
            }

# HTTP Get Call to Helix to retrieve Records
HttpResponse = requests.get(config.GetIncDataUrl, headers=HttpHeaders)
response_data=HttpResponse.json()

for entry in response_data['entries']:
                    values = entry['values']
                    reference = values['Incident Number']
                    content = "Incident Number : " + str(values['Incident Number']) + "\n Summary: " + str(values['Description']) + "\n Notes: " + str(values['Detailed Decription']) + "\n Resolution:" + str(values['Resolution']) + "\n Categorization Tier 1 :" + str(values['Categorization Tier 1']) +  "\n Categorization Tier 2 :" + str(values['Categorization Tier 2']) +  "\n Categorization Tier 3 :" + str(values['Categorization Tier 3']) + "\n Product Categorization Tier 1 :" + str(values['Product Categorization Tier 1']) + "\n Product Categorization Tier 2 :" + str(values['Product Categorization Tier 2']) + "\n Product Categorization Tier 3 :" + str(values['Product Categorization Tier 3']) + "\n Resolution  Category :" + str(values['Resolution Category']) + "\n Resolution Category Tier 2 :" + str(values['Resolution Category Tier 2']) + "\n Resolution Category Tier 3 :" + str(values['Resolution Category Tier 3']) + "\n Closure Product Category Tier 1 :" + str(values['Closure Product Category Tier1']) + "\n Closure Product Category Tier 2 :" + str(values['Closure Product Category Tier2']) + "\n Closure Product Category Tier 3 :" + str(values['Closure Product Category Tier3'])
                    print(content)
                    data = ('Helix', reference, content)                
                    # Insert records in Databse table
                    insertrecord(conn, data)
                    counter = counter + 1
                     #close database connection
conn.close()

print("Records Loaded" + str(counter))
  

#loadDataFromHelix()
#return {"Status" : "Success", "Records Loaded" : str(counter)} , 200
#return {"error": "Request must be JSON"}, 415  