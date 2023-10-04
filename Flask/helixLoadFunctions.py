import time
import threading
import requests
from Auth import GetAuthToken as Auth
import validateDataLoad as val
import SQL_Functions as sq
import generateEmbeding as ge
import DataLoadLogging as logs
import validateDataLoad as val
import configs as config

def loadFromHelixFull():
    source = "HELIX"
    initiateLoad = val.validateLoad(source)
    if initiateLoad:
        logs.writeLog(f"Full Data Load Initiated for Data Source:{source}.", "INFO")      
        threading.Thread(target=helixLoadFull).start()
        httpResponse = "Full Data Load Initiated from source:" + source +", check logs for more details."
    else:
        logs.writeLog(f"Previous DataLoad from source: {source} not completed yet, wait for previous load completion.", "ERROR")
        logs.writeLog("Data Load Terminated.", "ERROR")
        httpResponse = "Previous DataLoad from source: " + source + " not completed yet, wait for previous load completion."
    response = httpResponse
    return response
#---------------------------------------------------------------------------------------------------------------------------------------
def loadHelixDataDelta():
    source = "HELIX"
    initiateLoad = val.validateLoad(source)
    if initiateLoad:
        logs.writeLog(f"Delta Data Load Initiated for Data Source:{source}.", "INFO")      
        threading.Thread(target=helixLoadDelta).start()
        httpResponse = "Delta Data Load Initiated from source:"+ source + ", check logs for more details."
    else:
        logs.writeLog(f"Previous DataLoad from source: {source} not completed yet, wait for previous load completion.", "ERROR")
        logs.writeLog("Data Load Terminated.", "ERROR")
        httpResponse = "Previous DataLoad from source: " + source + " not completed yet, wait for previous load completion."
    response = httpResponse
    return response

def helixLoadDelta():
    # Get details of Helix forms and URLs
    helixDetails = config.helixDetails
    logs.writeLog("In HelixLoad Function.", "INFO")
    source = "HELIX"
    LoadType = "DELTA" 
    loadHistoryResults = val.createLoadHistoryInDB(source)
    loadTimestamp = loadHistoryResults[0]
    loadStatus=loadHistoryResults[1]
    recordCount = 0
    # Do something asynchronous here.
    # await asyncio.sleep(1)
    start_time = time.time()
    for form in helixDetails:
        url = helixDetails[form]
        args = (source, form, url, loadTimestamp, LoadType)
        recordCount+=loadHelixRecords(args)
        #threading.Thread(target=helix.loadHelixRecords(args)).start()
    
    if loadStatus == "Running":
        loadStatus = "Completed"
        args = (loadStatus, source, loadTimestamp)
        val.updateLoadHistory(args)
    end_time = time.time()
    # Calculate the execution time
    execution_time = end_time - start_time
    logs.writeLog(f"Records loaded in database: {recordCount}", "INFO")
    logs.writeLog(f"DataLoad Finished in {execution_time:.6f} seconds.", "INFO")
    print(f"Execution Time: {execution_time:.6f} seconds.") 
#-------------------------------------------------------------------#

def helixLoadFull():
    # Get details of Helix forms and URLs
    helixDetails = config.helixDetails
    logs.writeLog("In HelixLoad Function.", "INFO")
    source = "HELIX"
    LoadType = "FULL" 
    loadHistoryResults = val.createLoadHistoryInDB(source)
    loadTimestamp = loadHistoryResults[0]
    loadStatus=loadHistoryResults[1]
    recordCount = 0
    # Do something asynchronous here.
    # await asyncio.sleep(1)
    start_time = time.time()
    for form in helixDetails:
        url = helixDetails[form]
        args = (source, form, url, loadTimestamp, LoadType)
        recordCount+=loadHelixRecords(args)
        #threading.Thread(target=helix.loadHelixRecords(args)).start()
    
    if loadStatus == "Running":
        loadStatus = "Completed"
        args = (loadStatus, source, loadTimestamp)
        val.updateLoadHistory(args)
    end_time = time.time()
    # Calculate the execution time
    execution_time = end_time - start_time
    logs.writeLog(f"Records loaded in database: {recordCount}", "INFO")
    logs.writeLog(f"DataLoad Finished in {execution_time:.6f} seconds.", "INFO")
    print(f"Execution Time: {execution_time:.6f} seconds.") 
#-------------------------------------------------------------------#

def loadHelixRecords(args):
    #Extract arguments
    source = args[0]
    form = args[1]
    url = args[2]
    lastLoadTimestamp = args[3]
    load_type = args[4]
    
    # Initialize Variables
    offset  = 0
    limit = 1000  
    recordsExist = False
    recordCount = 0
    getrecords = True
    logs.writeLog(f"Data Load process started for records in " + form + " form.", "INFO")
    print("\nProcessing records for " + form + " form.")    
    while getrecords: 
        query_params = (url, offset, limit, lastLoadTimestamp, load_type)
 #       print (query_params)
        response_data = getRecords(query_params)        
        recordsExist = len(response_data["entries"]) > 0
        
        # This section is for debugging, comment this if..else later
        if recordsExist:
            getrecords = True    
            offset = offset + limit                         
        else:
            getrecords = False
            break            
        
        # This is important and it calls the function to load data into Database
        if recordsExist:
            args = (source, response_data, form)
            recordCount+=loadDataInDB(args)
    
    return recordCount    
#-----------------------------------------------------------------------------------------------

def getRecords(query_params):
        #Extract arguments
        url = query_params[0]
        offset = query_params[1]
        limit = query_params[2]
        load_timestamp = query_params[3]
        load_type = query_params[4]
    
#        print("Inside getRecords function", url, offset, limit, load_timestamp, load_type)   
        authToken = Auth()
        #print(authToken)
        if load_type == "FULL":
            url = url + "&offset=" + str(offset) + "&limit=" + str(limit)
        elif load_type == "DELTA" and "RKM:" not in url :
            url = url + "&offset=" + str(offset) + "&limit=" + str(limit) + "&q='Last Modified Date' > " + "\"" + load_timestamp + "\""
        elif load_type == "DELTA" and "RKM:" in url :
            url = url + "&offset=" + str(offset) + "&limit=" + str(limit) + "&q='Modified Date' > " + "\"" + load_timestamp + "\""
        
        # Prepare HTTP Headers for Helix Call
        httpHeaders = {
                'Authorization': authToken
            }
        httpResponse = requests.get(url, headers=httpHeaders)
        response_data = httpResponse.json()       
        
        return response_data
          
#-----------------------------------------------------------------
def loadDataInDB(args):
    # Extract arguments
    source = args[0]
    json_response = args[1]
    form = args[2]
    #print("In Load DB Function", args)
    # Initialize DB Connection
    conn = sq.getconnection()  
    dataRecords = []
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
        if form in {"KnowledgeHowTo", "KnowledgeKcs", "KnowledgeKe", "KnowledgePbm", "KnowledgeRef"}:
            reference = values['DocID']


        for key, value in values.items():
            if key not in {"Incident Number", "Infrastructure Change ID", "Work Order ID", "Problem Investigation ID", "Known Error ID", "DocID"}:
                record_data += str(value) +"\n"
            record_metadata += f"{key}: {value},\n"
                      
        # Code to slpit the contents in chunk s 
        # chunks = csplit.contentspiltter(record_data)      
        # for i, chunk in enumerate(chunks):
        #     content_parts = str(i+1)+ "/" + str(len(chunks))
        #     content_metadata = record_metadata
        #     content = chunk.page_content
        #     embedding = ge.generateEmbedding(content)
        #     embedding_list = embedding.tolist()
        #     #embeddings = ai.generateEmbeddings(content, "text-embedding-ada-002")
        #     #data = (source, filename, content, content_metadata, content_parts)
        #     data = (source, reference, content, content_metadata, content_parts, embedding_list[0])               
        #     # Insert records in Database table            
        #     sq.create_records(conn, data)
            
        # Code to slpit the contents based on Token limit          
        chunks = ge.generatetokens(record_data)
        
        for i, chunk in enumerate(chunks):
            content_parts = str(i+1)+ "/" + str(len(chunks))
            content_metadata = record_metadata
            content = chunk
            embedding = ge.generateEmbedding(content)
            embedding_list = embedding.tolist()
            #embeddings = ai.generateEmbeddings(content, "text-embedding-ada-002")
            #data = (source, filename, content, content_metadata, content_parts)
            data = (source, reference, content, content_metadata, content_parts, embedding_list[0])
            
            # Insert 1 record in Database table         
            #sq.createRecords(conn, data)
            
            # Insert bulk record in Database table
            dataRecords.append(data)
            count = len(dataRecords)
            
    sq.createBulkRecords(conn, dataRecords)   
    # Close DB Connection
    conn.close()
    
    return count
#-----------------------------------------------------------------    
