import requests
from SQL_Functions import create_connection as dbconnection
from SQL_Functions import create_record as insertrecord

def loadHelixRecords(form, url, helixToken):
    # Initialize Variables
    offset  = 0
    limit = 1000  
    recordsExist = False
    getrecords = True
    while getrecords:     
        response_data = getRecords(url, offset, limit, helixToken)
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
                    loadIncDataInDB(response_data)               
                if form == "IncidentWorkLog":
                    loadIncWLDataInDB(response_data)
                if form == "Change":    
                    loadCrqDataInDB(response_data)               
                if form == "ChangeWorkLog":
                    loadCrqWLDataInDB(response_data)
                if form == "WorkOrder":    
                    loadWoDataInDB(response_data)               
                if form == "WorkOrderWorkLog":
                    loadWoWLDataInDB(response_data)
                if form == "Problem":    
                    loadPbmDataInDB(response_data)               
                if form == "ProblemWorkLog":
                    loadPbmWLDataInDB(response_data)
                if form == "KnownError":    
                    loadPbmKEDataInDB(response_data)               
                if form == "KnownErrorWorkLog":
                    loadPbmKEWLDataInDB(response_data)
                if form == "Knowledge":
                    loadKmDataInDB(response_data)                    
        
                
#-----------------------------------------------------------------
  
def getRecords(url, offset , limit, token):
      # print("Inside getRecords function")   
        url = url + "&offset=" + str(offset) + "&limit=" + str(limit)
        print ("URL : " + url)
        # Prepare HTTP Headers for Helix Call
        HttpHeaders = {
                'Authorization': token
            }
        HttpResponse = requests.get(url, headers=HttpHeaders)
        response = HttpResponse.json()
        return response
#-----------------------------------------------------------------
def loadIncDataInDB(json_response):
    # Initialize variables
    content_limit = 500
    content_len = 0
    # Initialize DB Connection
    conn = dbconnection()  
    for entry in json_response['entries']:
        values = entry['values']
        reference = values['Incident Number']        
        record_data = ""
        for key, value in values.items():
            record_data += f"{key}: {value},\n"

        content_len = len(record_data)
        content_splits, content_rem = divmod(content_len, content_limit)
        if content_rem != 0:
            content_splits = content_splits + 1
        
        for split in range(content_splits):
            content = record_data[split * content_limit : (split + 1) * content_limit]                 
            content_parts = str(split+1) + "/" + str(content_splits)
            data = ('Helix', reference, content, content_parts)                
            # Insert records in Database table            
            insertrecord(conn, data)    
    
    # Close DB Connection
    conn.close()
#-----------------------------------------------------------------    
def loadIncWLDataInDB(json_response):
    # Initialize variables
    content_limit = 1000
    content_len = 0
    # Initialize DB Connection
    conn = dbconnection() 
    for entry in json_response['entries']:
        values = entry['values']
        reference = values['Incident Number'] + "_" + values['Work Log ID']
        record_data = "" 
        #print(record_data)
        for key, value in values.items():
            record_data += f"{key}: {value},\n"
                                
        content_len = len(record_data)
        content_splits, content_rem = divmod(content_len, content_limit)
        if content_rem != 0:
            content_splits = content_splits + 1
        
        for split in range(content_splits):
            content = record_data[split * content_limit : (split + 1) * content_limit]                 
            # print("Content")   
            content_parts = str(split+1) + "/" + str(content_splits)
            data = ('Helix', reference, content, content_parts)            
            # Insert records in Database table            
            insertrecord(conn, data)       
    # Close DB Connection
    conn.close()                               
#-----------------------------------------------------------------  
def loadCrqDataInDB(json_response):
    # Initialize variables
    content_limit = 500
    content_len = 0
    # Initialize DB Connection
    conn = dbconnection()  
    for entry in json_response['entries']:
        values = entry['values']
        reference = values['Infrastructure Change ID']        
        record_data = ""
        for key, value in values.items():
            record_data += f"{key}: {value},\n"

        content_len = len(record_data)
        content_splits, content_rem = divmod(content_len, content_limit)
        if content_rem != 0:
            content_splits = content_splits + 1
        
        for split in range(content_splits):
            content = record_data[split * content_limit : (split + 1) * content_limit]                 
            # print("Content")   
            content_parts = str(split+1) + "/" + str(content_splits)
            data = ('Helix', reference, content, content_parts)                
            # Insert records in Database table            
            insertrecord(conn, data)    
    
    # Close DB Connection
    conn.close()
#-----------------------------------------------------------------    
def loadCrqWLDataInDB(json_response):
    # Initialize variables
    content_limit = 1000
    content_len = 0
    # Initialize DB Connection
    conn = dbconnection() 
    for entry in json_response['entries']:
        values = entry['values']
        reference = values['Infrastructure Change ID'] + "_" + values['Work Log ID']
        record_data = "" 
        #print(record_data)
        for key, value in values.items():
            record_data += f"{key}: {value},\n"
                                
        content_len = len(record_data)
        content_splits, content_rem = divmod(content_len, content_limit)
        if content_rem != 0:
            content_splits = content_splits + 1
        
        for split in range(content_splits):
            content = record_data[split * content_limit : (split + 1) * content_limit]                 
            content_parts = str(split+1) + "/" + str(content_splits)
            data = ('Helix', reference, content, content_parts)            
            # Insert records in Database table            
            insertrecord(conn, data)       
    # Close DB Connection
    conn.close()                               
#-----------------------------------------------------------------  
def loadWoDataInDB(json_response):
    # Initialize variables
    content_limit = 500
    content_len = 0
    # Initialize DB Connection
    conn = dbconnection()  
    for entry in json_response['entries']:
        values = entry['values']
        reference = values['Work Order ID']        
        record_data = ""
        for key, value in values.items():
            record_data += f"{key}: {value},\n"

        content_len = len(record_data)
        content_splits, content_rem = divmod(content_len, content_limit)
        if content_rem != 0:
            content_splits = content_splits + 1
        
        for split in range(content_splits):
            content = record_data[split * content_limit : (split + 1) * content_limit]                 
            # print("Content")   
            content_parts = str(split+1) + "/" + str(content_splits)
            data = ('Helix', reference, content, content_parts)                
            # Insert records in Database table            
            insertrecord(conn, data)    
    
    # Close DB Connection
    conn.close()
#-----------------------------------------------------------------    
def loadWoWLDataInDB(json_response):
    # Initialize variables
    content_limit = 1000
    content_len = 0
    # Initialize DB Connection
    conn = dbconnection() 
    for entry in json_response['entries']:
        values = entry['values']
        reference = values['Work Order ID'] + "_" + values['Work Log ID']
        record_data = "" 
        #print(record_data)
        for key, value in values.items():
            record_data += f"{key}: {value},\n"
                                
        content_len = len(record_data)
        content_splits, content_rem = divmod(content_len, content_limit)
        if content_rem != 0:
            content_splits = content_splits + 1
        
        for split in range(content_splits):
            content = record_data[split * content_limit : (split + 1) * content_limit]                 
            content_parts = str(split+1) + "/" + str(content_splits)
            data = ('Helix', reference, content, content_parts)            
            # Insert records in Database table            
            insertrecord(conn, data)       
    # Close DB Connection
    conn.close()                               
#-----------------------------------------------------------------
def loadPbmDataInDB(json_response):
    # Initialize variables
    content_limit = 500
    content_len = 0
    # Initialize DB Connection
    conn = dbconnection()  
    for entry in json_response['entries']:
        values = entry['values']
        reference = values['Problem Investigation ID']        
        record_data = ""
        for key, value in values.items():
            record_data += f"{key}: {value},\n"

        content_len = len(record_data)
        content_splits, content_rem = divmod(content_len, content_limit)
        if content_rem != 0:
            content_splits = content_splits + 1
        
        for split in range(content_splits):
            content = record_data[split * content_limit : (split + 1) * content_limit]                 
            # print("Content")   
            content_parts = str(split+1) + "/" + str(content_splits)
            data = ('Helix', reference, content, content_parts)                
            # Insert records in Database table            
            insertrecord(conn, data)    
    
    # Close DB Connection
    conn.close()
#-----------------------------------------------------------------    
def loadPbmWLDataInDB(json_response):
    # Initialize variables
    content_limit = 1000
    content_len = 0
    # Initialize DB Connection
    conn = dbconnection() 
    for entry in json_response['entries']:
        values = entry['values']
        reference = values['Problem Investigation ID'] + "_" + values['Work Log ID']
        record_data = "" 
        #print(record_data)
        for key, value in values.items():
            record_data += f"{key}: {value},\n"
                                
        content_len = len(record_data)
        content_splits, content_rem = divmod(content_len, content_limit)
        if content_rem != 0:
            content_splits = content_splits + 1
        
        for split in range(content_splits):
            content = record_data[split * content_limit : (split + 1) * content_limit]                 
            content_parts = str(split+1) + "/" + str(content_splits)
            data = ('Helix', reference, content, content_parts)            
            # Insert records in Database table            
            insertrecord(conn, data)       
    # Close DB Connection
    conn.close()                               
#-----------------------------------------------------------------
def loadPbmKEDataInDB(json_response):
    # Initialize variables
    content_limit = 500
    content_len = 0
    # Initialize DB Connection
    conn = dbconnection()  
    for entry in json_response['entries']:
        values = entry['values']
        reference = values['Known Error ID']        
        record_data = ""
        for key, value in values.items():
            record_data += f"{key}: {value},\n"

        content_len = len(record_data)
        content_splits, content_rem = divmod(content_len, content_limit)
        if content_rem != 0:
            content_splits = content_splits + 1
        
        for split in range(content_splits):
            content = record_data[split * content_limit : (split + 1) * content_limit]                 
            # print("Content")   
            content_parts = str(split+1) + "/" + str(content_splits)
            data = ('Helix', reference, content, content_parts)                
            # Insert records in Database table            
            insertrecord(conn, data)    
    
    # Close DB Connection
    conn.close()
#-----------------------------------------------------------------    
def loadPbmKEWLDataInDB(json_response):
    # Initialize variables
    content_limit = 1000
    content_len = 0
    # Initialize DB Connection
    conn = dbconnection() 
    for entry in json_response['entries']:
        values = entry['values']
        reference = values['Known Error ID'] + "_" + values['Work Log ID']
        record_data = "" 
        #print(record_data)
        for key, value in values.items():
            record_data += f"{key}: {value},\n"
                                
        content_len = len(record_data)
        content_splits, content_rem = divmod(content_len, content_limit)
        if content_rem != 0:
            content_splits = content_splits + 1
        
        for split in range(content_splits):
            content = record_data[split * content_limit : (split + 1) * content_limit]                 
            content_parts = str(split+1) + "/" + str(content_splits)
            data = ('Helix', reference, content, content_parts)            
            # Insert records in Database table            
            insertrecord(conn, data)       
    # Close DB Connection
    conn.close()                               
#-----------------------------------------------------------------
def loadKmDataInDB(json_response):
    # Initialize variables
    content_limit = 1000
    content_len = 0
    # Initialize DB Connection
    conn = dbconnection() 
    for entry in json_response['entries']:
        values = entry['values']
        reference = values['DocID']
        record_data = "" 
        #print(record_data)
        for key, value in values.items():
            record_data += f"{key}: {value},\n"
                                
        content_len = len(record_data)
        content_splits, content_rem = divmod(content_len, content_limit)
        if content_rem != 0:
            content_splits = content_splits + 1
        
        for split in range(content_splits):
            content = record_data[split * content_limit : (split + 1) * content_limit]                 
            content_parts = str(split+1) + "/" + str(content_splits)
            data = ('Helix', reference, content, content_parts)            
            # Insert records in Database table            
            insertrecord(conn, data)       
    # Close DB Connection
    conn.close()                               
#-----------------------------------------------------------------