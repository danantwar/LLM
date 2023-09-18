import requests
import json
import datetime
from Auth import GetAuthToken as Auth
import openAIFunctions as ai
import SQL_Functions as sq
import contentSplitter as csplit
import generateEmbeding as ge

def loadHelixRecords(source, form, url, lastLoadTimestamp, load_type):
    # Initialize Variables
    offset  = 0
    limit = 1000  
    recordsExist = False
    recordCount = 0
    getrecords = True
    
    while getrecords:     
        response_data = getRecords(url, offset, limit, lastLoadTimestamp, load_type)
        recordsExist = len(response_data["entries"]) > 0
        
        # This section is for debugging, comment this if..else later
        if recordsExist:
            getrecords = True    
            offset = offset + limit             
            print("\nRecords found: " + form + "\n")    
        else:
            getrecords = False
            print("\nRecords not found: " + form + "\n")    
            break            
        
        # This is important and it calls the function to load data into Database
        if recordsExist:                 
            loadDataInDB(source, response_data, form)                    
    
    #print("Records Processed: ", recordCount)
    
#-----------------------------------------------------------------

def getRecords(url, offset, limit, load_timestamp, load_type):
      # print("Inside getRecords function")   
        authToken = Auth()
        if load_type == "FULL":
            url = url + "&offset=" + str(offset) + "&limit=" + str(limit)
        elif load_type == "DELTA" and "RKM:" not in url :
            url = url + "&offset=" + str(offset) + "&limit=" + str(limit) + "&q='Last Modified Date' > " + "\"" + load_timestamp + "\""
        elif load_type == "DELTA" and "RKM:" in url :
            url = url + "&offset=" + str(offset) + "&limit=" + str(limit) + "&q='Modified Date' > " + "\"" + load_timestamp + "\""
        
        # print ("URL : " + url)        
        # Prepare HTTP Headers for Helix Call
        HttpHeaders = {
                'Authorization': authToken
            }
        HttpResponse = requests.get(url, headers=HttpHeaders)
        response_data = HttpResponse.json()
        
        return response_data
    
#-----------------------------------------------------------------

def createLoadHistoryInDB(source):
    current_datetime = datetime.datetime.now(datetime.timezone.utc)
    loadTimestamp = current_datetime.strftime('%m/%d/%Y %H:%M:%S %p')
    loadStatus = "Running"
    conn = sq.getconnection() 
    data = (source, loadTimestamp, loadStatus)
    # Insert records in Database table
    sq.create_loadhistory(conn, data)
    conn.close()
    return loadTimestamp, loadStatus

#-----------------------------------------------------------------

def updateLoadHistory(loadStatus, source, loadTimestamp):
    conn = sq.getconnection() 
    data = (loadStatus, source, loadTimestamp)
    # Insert records in Database table
    sq.update_loadHistory(conn, data)
    conn.close()
        
#-----------------------------------------------------------------

def getLastLoadTimestamp(source):
    conn = sq.getconnection()
    query = "SELECT load_timestamp, load_status FROM public.\"LoadHistory\" WHERE source = '" + source + "' ORDER BY load_timestamp DESC LIMIT 1 "
    lastLoadTimestamp = ""
    loadStatus = ""

    try:
        cursor = conn.cursor()        
        cursor.execute(query)
        records = cursor.fetchall()
        for record in records:
            lastLoadTimestamp = record[0]
            loadStatus=record[1]
            print("Load History Record: ", record)
    except (Exception) as error:
        print("Error while reading records:", error)
    
    conn.close()
    return lastLoadTimestamp, loadStatus

#-----------------------------------------------------------------

def loadDataInDB(source, json_response, form):

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
            # Insert records in Database table            
            sq.create_records(conn, data)   

    # Close DB Connection
    conn.close()
#-----------------------------------------------------------------    
