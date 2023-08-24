# app.py
import configs as config
from Auth import GetAuthToken as Auth
from helixLoadFunctions import loadHelixRecords as loadHelixData
           
# Starting point of Execution                    

# Generate Helix Auth Token
helixToken= Auth()

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
    "Knowledge" : config.GetRkmKEUrl
    }
    
for form in HelixDetails:
    url = HelixDetails[form]   
   # print("Calling Process_records function")   
    loadHelixData(form, url, helixToken)
    #print("Records Loaded" + str(records_count))

