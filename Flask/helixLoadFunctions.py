import requests
import datetime
from Auth import GetAuthToken as Auth
from SQL_Functions import create_connection as dbconnection
from SQL_Functions import create_datarecords as loadrecord
from SQL_Functions import create_loadhistory as loadhistory
from SQL_Functions import read_records as getDBRecords
source = "HELIX"

def loadHelixRecords(form, url, load_type):
    # Initialize Variables
    offset  = 0
    limit = 1000  
    recordsExist = False
    getrecords = True
    timestamp = createLoadHistoryInDB()
    
    if load_type == "DELTA":
        timestamp = getLastLoadTimestamp()
        
    while getrecords:     
        response_data = getRecords(url, offset, limit, timestamp, load_type)
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
            loadDataInDB(response_data, form)                    
#-----------------------------------------------------------------
def getRecords(url, offset, limit, load_timestamp, load_type):
      # print("Inside getRecords function")   
        authToken = Auth()
        if load_type == "FULL":
            url = url + "&offset=" + str(offset) + "&limit=" + str(limit)
        elif load_type == "DELTA" and "Knowledge" not in url :
            url = url + "&offset=" + str(offset) + "&limit=" + str(limit) + "&q='Last Modified Date' > " + "\"" + load_timestamp + "\""
        elif load_type == "DELTA" and "Knowledge" in url :
            url = url + "&offset=" + str(offset) + "&limit=" + str(limit) + "&q='Modified Date' > " + "\"" + load_timestamp + "\""
        
        print ("URL : " + url)
        
        # Prepare HTTP Headers for Helix Call
        HttpHeaders = {
                'Authorization': authToken
            }
        HttpResponse = requests.get(url, headers=HttpHeaders)
        response = HttpResponse.json()
        print (response)
        return response
#-----------------------------------------------------------------
def createLoadHistoryInDB():
    current_datetime = datetime.datetime.now(datetime.timezone.utc)
    load_timestamp = current_datetime.strftime('%m/%d/%Y %H:%M:%S %p')
    conn = dbconnection() 
    data = (source, load_timestamp)                
    # Insert records in Database table            
    loadhistory(conn, data)
    conn.close()
    return load_timestamp
#-----------------------------------------------------------------
def getLastLoadTimestamp():
    conn = dbconnection()
    query = "SELECT load_timestamp FROM public.\"LoadHistory\" LIMIT 1"

    try:
        cursor = conn.cursor()        
        cursor.execute(query)
        records = cursor.fetchall()
        for record in records:
           load_timestamp = record[0]
    except (Exception) as error:
        print("Error while reading records:", error)
    
    conn.close()
    return load_timestamp
#-----------------------------------------------------------------
def loadDataInDB(json_response, form):
    # Initialize variables
    content_limit = 1000
    content_len = 0
    # Initialize DB Connection
    conn = dbconnection()  
    for entry in json_response['entries']:
        values = entry['values']
        record_data = ""
        if form == "Incident":    
            reference = values['Incident Number']
        if form == "IncidentWorkLog":
            reference = values['Incident Number'] + "_" + values['Work Log ID']
        if form == "Change":    
            reference = values['Infrastructure Change ID']
        if form == "ChangeWorkLog":
            reference = values['Infrastructure Change ID'] + "_" + values['Work Log ID']
        if form == "WorkOrder":    
            reference = values['Work Order ID']
        if form == "WorkOrderWorkLog":
            reference = values['Work Order ID'] + "_" + values['Work Log ID']
        if form == "Problem":    
            reference = values['Problem Investigation ID']
        if form == "ProblemWorkLog":
            reference = values['Problem Investigation ID'] + "_" + values['Work Log ID']
        if form == "KnownError":    
            reference = values['Known Error ID']
        if form == "KnownErrorWorkLog":
            reference = values['Known Error ID'] + "_" + values['Work Log ID']
        if form == "Knowledge":
            reference = values['DocID']
                    
        for key, value in values.items():
            record_data += f"{key}: {value},\n"

        content_len = len(record_data)
        content_splits, content_rem = divmod(content_len, content_limit)
        if content_rem != 0:
            content_splits = content_splits + 1
        
        for split in range(content_splits):
            content = record_data[split * content_limit : (split + 1) * content_limit]                 
            content_parts = str(split+1) + "/" + str(content_splits)
            data = (source, reference, content, content_parts)                
            # Insert records in Database table            
            loadrecord(conn, data)    
    
    # Close DB Connection
    conn.close()
#-----------------------------------------------------------------    
