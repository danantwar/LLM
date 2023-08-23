# app.py
import requests
import configs as config
from Auth import GetAuthToken as Auth
from SQL_Functions import create_connection as dbconnection
from SQL_Functions import create_record as insertrecord
#from flask import Flask, request, jsonify
#from datetime import datetime

def process_records(form, url):
    # print("Inside Process_records function")   
    # Initialize Varibales
    offset  = 0
    limit = 1000  
    recordsExist = False
    getrecords = True
    while getrecords:
        getRecords(url, offset, limit)            
        response_data = getRecords(url, offset, limit)
        entries_count = len(response_data["entries"])
        
        if entries_count != 0:
            getrecords = True    
            recordsExist = True
            offset = offset + limit             
            print("\nRecord Exist Flag : " + str(recordsExist) + "\n")    
        else:
            recordsExist = False
            getrecords = False
            print("\nRecord Exist Flag : " + str(recordsExist) + "\n")    
            break
            
        
        if recordsExist:
                if form == "Incident":    
                    loadIncdataInDB(response_data)               
                if form == "IncidentWorkLog":
                    loadIncWLdataInDB(response_data)
        
                
#-----------------------------------------------------------------
  
def getRecords(url, offset , limit):
      # print("Inside getRecords function")   
        url = url + "&offset=" + str(offset) + "&limit=" + str(limit)
        print ("URL : " + url)
        HttpResponse = requests.get(url, headers=HttpHeaders)
        response = HttpResponse.json()
        return response
#-----------------------------------------------------------------
    
def loadIncdataInDB(json_response):
   # print("Inside loadIncdataInDB function")   
    # Initialize variables
    content_limit = 500
    content_len = 0
    # Initialize DB Connection
    conn = dbconnection()  
    for entry in json_response['entries']:
      # print("Inside For Loop of loadIncdataInDB function")   
        values = entry['values']
        reference = values['Incident Number']
        IncContent = "Incident Number : " + str(values['Incident Number']) + "\nSummary: " + str(values['Description']) + "\nNotes: " + str(values['Detailed Decription']) + "\nResolution:" + str(values['Resolution']) + "\nCategorization Tier 1 :" + str(values['Categorization Tier 1']) +  "\nCategorization Tier 2 :" + str(values['Categorization Tier 2']) +  "\nCategorization Tier 3 :" + str(values['Categorization Tier 3']) + "\nProduct Categorization Tier 1 :" + str(values['Product Categorization Tier 1']) + "\nProduct Categorization Tier 2 :" + str(values['Product Categorization Tier 2']) + "\nProduct Categorization Tier 3 :" + str(values['Product Categorization Tier 3']) + "\nResolution  Category :" + str(values['Resolution Category']) + "\nResolution Category Tier 2 :" + str(values['Resolution Category Tier 2']) + "\nResolution Category Tier 3 :" + str(values['Resolution Category Tier 3']) + "\nClosure Product Category Tier 1 :" + str(values['Closure Product Category Tier1']) + "\nClosure Product Category Tier 2 :" + str(values['Closure Product Category Tier2']) + "\nClosure Product Category Tier 3 :" + str(values['Closure Product Category Tier3'])
        #print(content)
        content_len = len(IncContent)
        content_splits, content_rem = divmod(content_len, content_limit)
        if content_rem != 0:
            content_splits = content_splits + 1
        
        for split in range(content_splits):
            content = IncContent[split * content_limit : (split + 1) * content_limit]                 
            # print("Content")   
            content_parts = str(split+1) + "#" + str(content_splits)
            data = ('Helix', reference, content, content_parts)                
            # Insert records in Database table            
            insertrecord(conn, data)    
    
    # Close DB Connection
    conn.close()
#-----------------------------------------------------------------
    
def loadIncWLdataInDB(json_response):
    # Initialize variables
    content_limit = 1000
    content_len = 0
    # Initialize DB Connection
    conn = dbconnection() 
    for entry in json_response['entries']:
        values = entry['values']
        reference = values['Incident Number'] + "_" + values['Work Log ID']
        IncWLContent = "Incident Number : " + str(values['Incident Number']) + "\nWork Log ID : " + str(values['Work Log ID']) + "\nWorkLog Summary : " + str(values['Description']) + "\nWorkLog Notes : " + str(values['Detailed Description']) 
        #print(IncWLContent)
        content_len = len(IncWLContent)
        content_splits, content_rem = divmod(content_len, content_limit)
        if content_rem != 0:
            content_splits = content_splits + 1
        
        for split in range(content_splits):
            content = IncWLContent[split * content_limit : (split + 1) * content_limit]                 
            # print("Content")   
            content_parts = str(split+1) + "#" + str(content_splits)
            data = ('Helix', reference, content, content_parts)            
            # Insert records in Database table            
            insertrecord(conn, data)       
    # Close DB Connection
    conn.close()                               
#-----------------------------------------------------------------    
                   
# Starting point of Execution                    

# Generate Helix Auth Token
helixToken= Auth()

# Prepare HTTP Headers for Helix Call
HttpHeaders = {
                'Authorization': helixToken
            }

# Get details of Helix forms and URLs
HelixDetails = {
    "Incident": config.GetIncDataUrl,
    "IncidentWorkLog":config.GetIncWorkLogsUrl
    }
    
for form in HelixDetails:
    url = HelixDetails[form]   
   # print("Calling Process_records function")   
    process_records(form, url)
    #print("Records Loaded" + str(records_count))
