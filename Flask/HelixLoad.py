# app.py
import asyncio
import configs as config
import helixLoadFunctions as helix         
            
#load_type = "FULL"
#load_type = "DELTA"
def initiateHelixLoad(LoadType):    
    source = "HELIX"    
    loadHistoryResults = helix.getLastLoadTimestamp(source)     
    lastLoadTimestamp = loadHistoryResults[0]
    loadStatus=loadHistoryResults[1]
    print("Last Load Status: ", loadStatus)
    if (loadStatus == "Completed" or loadStatus == ""):
        initiateLoad = True
    else:
        initiateLoad = False
        
    if initiateLoad:
        result = asyncio.run(helixLoad(initiateLoad, source, LoadType))
        response = f"DataLoad Initiated for {source}, check logs for more details."
    else:
        response = f"Previous DataLoad for {source} has not completed yet, wait for previous load completion."
    print(response)    
    return response

#-------------------------------------------------------------------#

async def helixLoad(initiateLoad, source, LoadType):
    # Get details of Helix forms and URLs
    HelixDetails = {
        "Incident" : config.GetIncDataUrl,
        "IncidentWorkLog" : config.GetIncWorkLogsUrl,
        "Change" : config.GetCrqUrl,
        "ChangeWorkLog" : config.GetCrqWLUrl,
        "WorkOrder" : config.GetWoUrl,
        "WorkOrderWorkLog" : config.GetWoWLUrl,
        "Problem" : config.GetPbmUrl,
        "ProblemWorkLog" : config.GetPbmWLUrl,
        "KnownError" : config.GetPbmKEUrl,
        "KnownErrorWorkLog" : config.GetPbmKEWLUrl,
        "KnowledgeHowTo" : config.GetRkmHowToUrl,
        "KnowledgeKcs" : config.GetRkmKcsUrl,
        "KnowledgeKe" : config.GetRkmKEUrl,
        "KnowledgePbm" : config.GetRkmPbmUrl,
        "KnowledgeRef" : config.GetRkmRefUrl,
    }

    if initiateLoad:    
        loadHistoryResults = helix.createLoadHistoryInDB(source)
        loadTimestamp = loadHistoryResults[0]
        loadStatus=loadHistoryResults[1]
        for form in HelixDetails:
            url = HelixDetails[form]   
            helix.loadHelixRecords(source, form, url, loadTimestamp, LoadType)
        
        if loadStatus == "Running":
            loadStatus = "Completed"
            helix.updateLoadHistory(loadStatus, source, loadTimestamp)
