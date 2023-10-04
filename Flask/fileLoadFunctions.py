import openAIFunctions as ai
import SQL_Functions as sq
import datetime
import contentSplitter as csplit
import generateEmbeding as ge
import fileReadFunctions as frf
from werkzeug.utils import secure_filename
import os
import validateDataLoad as val
import DataLoadLogging as logs
import time
import threading

def dataLoadFromFile(inputFile):
    # Get the file from the request
    file = inputFile
    # Save the file to a temporary location
    filename = secure_filename(file.filename)
    dataExists = checkDataExists(filename)   
    if dataExists:
        logs.writeLog(f"Data already exist in database for {filename} , please try data load for any other File.", "ERROR")
        logs.writeLog("Data Load Terminated.", "ERROR")
        httpResponse = f"Data already exist in database for {filename} , please try data load for any other File."
    else:
        logs.writeLog(f"Data Load Initiated from File: {filename}", "INFO")    
        print("I am in else")  
        flResponse = loadFromFile(inputFile)
        if flResponse > 0:
            httpResponse = f"Data Loaded from File:{filename} successfully. Total {flResponse} records created in database."
        else:
            httpResponse = f"Data Load from File:{filename} has failed, please check logs for more details."
    return httpResponse
#--------------------------------------------------------------------------------------------------------------------------
def checkDataExists(filename):
    conn = sq.getconnection()
    query = "SELECT content FROM public.\"LLM\" WHERE reference = '" + filename + "'"

    try:
        cursor = conn.cursor()        
        cursor.execute(query)
        records = cursor.fetchall()
        if records:
            dataExists = True
        else:
            dataExists = False
    except (Exception) as error:
        print("Error while reading records:", error)
  
    conn.close()
    return dataExists
#-----------------------------------------------------------------

def loadFromFile(inputFile):
    
    #Initialize Variables
    source = "FILE"
    
    # Get the file from the request
    file = inputFile
   
    # Save the file to a temporary location
    filename = secure_filename(file.filename)
    temp_folder = 'C:\\Users\\jagadish.patil\\myTestEnv\\tempFiles'
    file.save(os.path.join(temp_folder, filename))
    
      # Load the contents of the file into a string
    file_path = os.path.join(temp_folder, filename)
    file_content = frf.read_file_content(file_path)

    # Add enty in history table for this file
    loadHistoryResults = val.createLoadHistoryInDB(source)
    loadTimestamp = loadHistoryResults[0]
    loadStatus=loadHistoryResults[1]
    recordCount = 0
    start_time = time.time()

    # Load content in database
    recordscount=loadDataInDB(source, filename, file_content)
    
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
    return recordscount

#-----------------------------------------------------------------
def loadDataInDB(source, filename, file_content):
    dataRecords = []
    count=0
     # Initialize DB Connection    
    conn = sq.getconnection()
    
    # Code to slpit the contents based on Token limit  
    chunks = ge.generatetokens(file_content)
    for i, chunk in enumerate(chunks):
        content_parts = str(i+1)+ "/" + str(len(chunks))
        content_metadata = chunk
        content = chunk
        embedding = ge.generateEmbedding(content)
        embedding_list = embedding.tolist()
        data = (source, filename, content, content_metadata, content_parts, embedding_list[0])                
        # Insert records in Database table
        dataRecords.append(data)
        
    count = len(dataRecords)
    sq.createBulkRecords(conn, dataRecords)              
    # sq.create_records(conn, data)
    # print ("Parts: " + str(len(chunks)))
    
    # Close DB Connection
    conn.close()
    return count
#----------------------------------------------------------------- 

# def loadFileinBulk(file_name, file_Path):
    
#     #Initialize Variables
#     source = "FILE"
    
#     file_content = frf.read_file_content(file_Path)

#     # Add enty in history table for this file
#     fl.addLoadHistoryInDB(source)
#     file_content = file_content.replace('\r', '').replace('\n', '')
#     #file_content = file_content.replace('\xa0', ' ')
#     # Load content in database
#     fl.loadDataInDB (source, file_name, file_content)