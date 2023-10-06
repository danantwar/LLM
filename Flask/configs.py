# This file contains configuration values used in all other python files

# Database Connectivity details
dbuser="postgres"
dbpassword="postgres"
host="localhost"
port="5435"
database="postgres"


# Helix API endpoint URLs and Credentials
BaseUrl = 'https://helixsjc814-demo-restapi.onbmc.com/api/arsys/v1/entry/'
AuthUrl = 'https://helixsjc814-demo-restapi.onbmc.com/api/jwt/login'
username = 'Seth'
password = 'Password_1234'

# Directory path used for data load using FILE
KB_dir = 'C:\\tmp\\LLM\\KBs'
dataFile_dir = 'C:\\tmp\\LLM\\DataFiles'
archive_dir = 'C:\\tmp\\LLM\\Archived'
log_file = 'logs\dataload.log'

# Define the token limit for model tokenizer
model_token_limit = 500

# Helix Form Names
INC_Url = 'HPD:Help Desk'
INC_WorkLogUrl = 'HPD:WorkLog'
CRQ_Url = 'CHG:Infrastructure Change'
CRQ_WorkLogsUrl = 'CHG:WorkLog'
PBM_Url = 'PBM:Problem Investigation'
PBM_WorkLogsUrl = 'PBM:Investigation WorkLog'
PBMKE_URL = "PBM:Known Error"
PBMKE_WorkLog_URL = "PBM:Known Error WorkLog"
WO_Url = 'WOI:WorkOrder'
WO_WorkLogsUrl = 'WOI:WorkInfo'
KM_Url= 'RKM:KnowledgeArticleManager'
KM_HowToUrl = 'RKM:HowToTemplate_Manageable_Join'
KM_KcsUrl = 'RKM:KCS:Template_Manageable_Join'
KM_KeUrl = 'RKM:KnownErrorTemplate_Manageable_Join'
KM_PbmUrl = 'RKM:ProblemSolutionTemplate_Manageable_Join'
KM_RefUrl = 'RKM:ReferenceTemplate_Manageable_Join'

# Incident fields to be retrieved in Query
IncidentFieldList = "?fields=values(Incident Number, Description, Detailed Decription, Resolution)"
# Construct Url to fetch Incident Details
GetIncDataUrl= BaseUrl+INC_Url+IncidentFieldList

# Incident WorkLog fields to be retrieved in Query
WorkLogFieldList = '?fields=values(Incident Number, Work Log ID, Description, Detailed Description)'
# Construct Url to fetch Incident Worklog Details
GetIncWorkLogsUrl= BaseUrl + INC_WorkLogUrl + WorkLogFieldList

# Change fields to be retrieved in Query
CrqFieldList = "?fields=values(Infrastructure Change ID, Description, Detailed Description)"
# Construct Url to fetch Change Details
GetCrqUrl= BaseUrl+CRQ_Url+CrqFieldList

# Change WorkLog fields to be retrieved in Query
CrqWLFieldList = "?fields=values(Infrastructure Change ID, Work Log ID, Description, Detailed Description)"
# Construct Url to fetch Change Worklog Details
GetCrqWLUrl= BaseUrl + CRQ_WorkLogsUrl + CrqWLFieldList

# WorkOrder fields to be retrieved in Query
WoFieldList = "?fields=values(Work Order ID, Summary, Detailed Description)"
# Construct Url to fetch Work order Details
GetWoUrl= BaseUrl+WO_Url+WoFieldList

# WorkOrder WorkLog fields to be retrieved in Query
WoWLFieldList = "?fields=values(Work Order ID, Work Log ID, Description, Detailed Description)"
# Construct Url to fetch Work order Worklog Details
GetWoWLUrl= BaseUrl+WO_WorkLogsUrl+WoWLFieldList

# Problem fields to be retrieved in Query
PbmFieldList = "?fields=values(Problem Investigation ID, Description, Detailed Decription, Temporary Workaround, Implemented Solution)"
# Construct Url to fetch Problem Details
GetPbmUrl= BaseUrl+PBM_Url+PbmFieldList

# Problem WorkLog fields to be retrieved in Query
PbmWLFieldList = "?fields=values(Problem Investigation ID, Work Log ID, Description, Detailed Description)"
# Construct Url to fetch Problem Worklog Details
GetPbmWLUrl= BaseUrl+PBM_WorkLogsUrl+PbmWLFieldList

# Known Error fields to be retrieved in Query
PbmKEFieldList = "?fields=values(Known Error ID, Description, Detailed Decription, Temporary Workaround, Resolution)"
# Construct Url to fetch Knon Error Details
GetPbmKEUrl= BaseUrl+PBMKE_URL+PbmKEFieldList

# Known Error WorkLog fields to be retrieved in Query
PbmKEWLFieldList = "?fields=values(Known Error ID, Work Log ID, Description, Detailed Description)"
# Construct Url to fetch Known Error Worklog Details
GetPbmKEWLUrl= BaseUrl+ PBMKE_WorkLog_URL +PbmKEWLFieldList

# Knowledge Mgmt fields and URLs to retrieve details for Knowledge articles in helix
KM_HowToFieldList = "?fields=values(DocID, Article_Keywords,RKMTemplateQuestion,RKMTemplateAnswer,RKMTemplateTechnicianNotes)"
GetRkmHowToUrl= BaseUrl+KM_HowToUrl+KM_HowToFieldList
KM_KcsFieldList = "?fields=values(DocID, Article_Keywords,RKMTemplateKCSProblem,RKMTemplateEnvironment,RKMTemplateResolution,RKMTemplateCause)"
GetRkmKcsUrl= BaseUrl+KM_KcsUrl+KM_KcsFieldList
KM_KeFieldList = "?fields=values(DocID, Article_Keywords,RKMTemplateError,RKMTemplateFix,RKMTemplateRootCause,RKMTemplateTechnicianNotes)"
GetRkmKEUrl= BaseUrl+KM_KeUrl+KM_KeFieldList
KM_PbmFieldList = "?fields=values(DocID, Article_Keywords,RKMTemplateProblem,RKMTemplateSolution,RKMTemplateTechnicianNotes)"
GetRkmPbmUrl= BaseUrl+KM_PbmUrl+KM_PbmFieldList
KM_RefFieldList = "?fields=values(DocID, Article_Keywords,Reference)"
GetRkmRefUrl= BaseUrl+KM_RefUrl+KM_RefFieldList

# Helix URLs mapping with respective module and forms
helixDetails = {
    "Incident" : GetIncDataUrl,
    "IncidentWorkLog" : GetIncWorkLogsUrl,
    "Change" : GetCrqUrl,
    "ChangeWorkLog" : GetCrqWLUrl,
    "WorkOrder" : GetWoUrl,
    "WorkOrderWorkLog" : GetWoWLUrl,
    "Problem" : GetPbmUrl,
    "ProblemWorkLog" : GetPbmWLUrl,
    "KnownError" : GetPbmKEUrl,
    "KnownErrorWorkLog" : GetPbmKEWLUrl,
    "KnowledgeHowTo" : GetRkmHowToUrl,
    "KnowledgeKcs" : GetRkmKcsUrl,
    "KnowledgeKe" : GetRkmKEUrl,
    "KnowledgePbm" : GetRkmPbmUrl,
    "KnowledgeRef" : GetRkmRefUrl,
 }