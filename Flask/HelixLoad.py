# app.py
import time
import configs as config
import helixLoadFunctions as helix        
import DataLoadLogging as logs

#load_type = "FULL"
#load_type = "DELTA"

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

    initiateLoad = args[0]
    source = args[1]
    LoadType = args[2]
    
    if initiateLoad:    
        loadHistoryResults = helix.createLoadHistoryInDB(source)
        loadTimestamp = loadHistoryResults[0]
        loadStatus=loadHistoryResults[1]
        start_time = time.time()
        for form in HelixDetails:
            url = HelixDetails[form]
            helix.loadHelixRecords(source, form, url, loadTimestamp, LoadType)
        
        if loadStatus == "Running":
            loadStatus = "Completed"
            helix.updateLoadHistory(loadStatus, source, loadTimestamp)
        end_time = time.time()
        # Calculate the execution time
        execution_time = end_time - start_time
        logs.writeLog(f"DataLoad Finished in {execution_time:.6f} seconds.", "INFO")
        print(f"Execution Time: {execution_time:.6f} seconds.") 
#-------------------------------------------------------------------#
