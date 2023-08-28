# app.py
import configs as config
import helixLoadFunctions as helix
            
#load_type = "FULL"
#load_type = "DELTA"
def initiateHelixLoad(LoadType):
#    load_type = LoadType
    # Get details of Helix forms and URLs
    HelixDetails = {
#        "Incident" : config.GetIncDataUrl,
 #       "IncidentWorkLog" : config.GetIncWorkLogsUrl,
        "Change" : config.GetCrqUrl,
        "ChangeWorkLog" : config.GetCrqWLUrl,
        "WorkOrder" : config.GetWoUrl,
        "WorkOrderWorkLog" : config.GetWoWLUrl,
        "Problem" : config.GetPbmUrl,
        "ProblemWorkLog" : config.GetPbmWLUrl,
        "KnownError" : config.GetPbmKEUrl,
        "KnownErrorWorkLog" : config.GetPbmKEWLUrl,
        "Knowledge" : config.GetRkmKEUrl
    }
    
    for form in HelixDetails:
        url = HelixDetails[form]   
        # print("Calling Process_records function")
        helix.loadHelixRecords(form, url, LoadType)
        # print("Records Loaded" + str(records_count))

