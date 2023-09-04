import requests
import datetime
from Auth import GetAuthToken as Auth
import SQL_Functions as sq

def loadHelixRecords(form, url, load_type):
    # Initialize Variables
    source = "HELIX"
    offset  = 0
    limit = 1000  
    recordsExist = False
    getrecords = True
    timestamp = createLoadHistoryInDB(source)
    print(load_type)
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
            loadDataInDB(source, response_data, form)                    
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
        
        return response
#-----------------------------------------------------------------
def createLoadHistoryInDB(source):
    current_datetime = datetime.datetime.now(datetime.timezone.utc)
    load_timestamp = current_datetime.strftime('%m/%d/%Y %H:%M:%S %p')
    conn = sq.getconnection() 
    data = (source, load_timestamp)                
    # Insert records in Database table            
    sq.create_loadhistory(conn, data)
    conn.close()
    return load_timestamp
#-----------------------------------------------------------------
def getLastLoadTimestamp():
    conn = sq.getconnection()
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
def loadDataInDB(source, json_response, form):
    # Initialize variables
    # content_limit = 1000
    # content_len = 0   
    # Initialize DB Connection
    conn = sq.getconnection()  
    for entry in json_response['entries']:
        values = entry['values']
        record_data = ""
        record_metadata = ""
        if form == "Incident" or form == "IncidentWorkLog" :    
            reference = values['Incident Number']        
        if form == "Change" or form == "ChangeWorkLog":
            reference = values['Infrastructure Change ID']        
        if form == "WorkOrder" or form == "WorkOrderWorkLog":
            reference = values['Work Order ID']        
        if form == "Problem" or form == "ProblemWorkLog":
            reference = values['Problem Investigation ID']        
        if form == "KnownError" or form == "KnownErrorWorkLog":
            reference = values['Known Error ID']        
        if form == "Knowledge":
            reference = values['DocID']
                    
        for key, value in values.items():            
            record_data += str(value)
            record_metadata += f"{key}: {value},\n"
            
            
        '''
        # Code to slpit the contents in chunk
        content_len = len(record_data)
        content_splits, content_rem = divmod(content_len, content_limit)
        if content_rem != 0:
            content_splits = content_splits + 1
        
        for split in range(content_splits):
            content = record_data[split * content_limit : (split + 1) * content_limit]                 
            content_parts = str(split+1) + "/" + str(content_splits)
        '''    
        content_splits = "1/1"
        data = (source, reference, record_data, record_metadata, content_splits)
        # Insert records in Database table            
        sq.create_records(conn, data)    
    
    # Close DB Connection
    conn.close()
#-----------------------------------------------------------------    
