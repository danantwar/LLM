# app.py
import time
import configs as config
import helixLoadFunctions as helix        
import DataLoadLogging as logs
import threading

#load_type = "FULL"
#load_type = "DELTA"

# def initiateHelixLoad(LoadType):    
#     source = "HELIX"    
#     loadHistoryResults = sq.getLastLoadTimestamp(source)     
#     lastLoadTimestamp = loadHistoryResults[0]
#     loadStatus=loadHistoryResults[1]
#     print("Last Load Status: ", loadStatus)
#     if (loadStatus == "Completed" or loadStatus == ""):
#         initiateLoad = True
#     else:
#         initiateLoad = False
        
#     if initiateLoad:
#         args = (initiateLoad, source, LoadType)
#         thread = threading.Thread(target=helix.helixLoad(args))
#         thread.start()
#         logs.writeLog(f"DataLoad Initiated for Data Source:{source}.", "INFO")
#         httpResponse = {"message" : f"DataLoad Initiated for {source}, check logs for more details."}
#         httpCode = 202
#     else:
#         httpResponse = {"error" : f"Previous DataLoad for {source} has not completed yet, wait for previous load completion."}
#         httpCode = 415
#         logs.writeLog(f"Previous DataLoad for {source} has not completed yet, wait for previous load completion.", "WARN")
#         logs.writeLog("Data Load Terminated.", "ERROR")
    
#     return httpResponse, httpCode
#--------------------------------------------------------------------------------------
def helixLoad(args):
    # Get details of Helix forms and URLs
    HelixDetails = {
        "Incident" : config.GetIncDataUrl
 #        "IncidentWorkLog" : config.GetIncWorkLogsUrl,
#         "Change" : config.GetCrqUrl,
#         "ChangeWorkLog" : config.GetCrqWLUrl,
#         "WorkOrder" : config.GetWoUrl,
#         "WorkOrderWorkLog" : config.GetWoWLUrl,
#         "Problem" : config.GetPbmUrl,
#         "ProblemWorkLog" : config.GetPbmWLUrl,
#         "KnownError" : config.GetPbmKEUrl,
#         "KnownErrorWorkLog" : config.GetPbmKEWLUrl,
#         "KnowledgeHowTo" : config.GetRkmHowToUrl,
#         "KnowledgeKcs" : config.GetRkmKcsUrl,
#         "KnowledgeKe" : config.GetRkmKEUrl,
#         "KnowledgePbm" : config.GetRkmPbmUrl,
#         "KnowledgeRef" : config.GetRkmRefUrl,
    }

    logs.writeLog("In HelixLoad Function.", "INFO")
    source = args[0]
    LoadType = args[1] 
    loadHistoryResults = helix.createLoadHistoryInDB(source)
    loadTimestamp = loadHistoryResults[0]
    loadStatus=loadHistoryResults[1]
    recordCount = 0
    # Do something asynchronous here.
    # await asyncio.sleep(1)
    start_time = time.time()
    for form in HelixDetails:
        url = HelixDetails[form]
        args = (source, form, url, loadTimestamp, LoadType)
        recordCount+=helix.loadHelixRecords(args)
        #threading.Thread(target=helix.loadHelixRecords(args)).start()
    
    if loadStatus == "Running":
        loadStatus = "Completed"
        args = (loadStatus, source, loadTimestamp)
        helix.updateLoadHistory(args)
    end_time = time.time()
    # Calculate the execution time
    execution_time = end_time - start_time
    logs.writeLog(f"Records loaded in database: {recordCount}", "INFO")
    logs.writeLog(f"DataLoad Finished in {execution_time:.6f} seconds.", "INFO")
    print(f"Execution Time: {execution_time:.6f} seconds.") 
#-------------------------------------------------------------------#
