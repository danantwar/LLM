# API endpoint URL

BaseUrl = 'https://helixsjc814-demo-restapi.onbmc.com/api/arsys/v1/entry/'
username = 'Seth'
password = 'Password_1234'
AuthUrl = 'https://helixsjc814-demo-restapi.onbmc.com/api/jwt/login'
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
KM_Url = 'RKM:KnowledgeArticleManager'

# Incident Query Parameters
#IncQueryQual = "?q='Incident Number'=\"INC000000024397\""
IncidentFieldList = "?fields=values(Incident Number, Description, Detailed Decription,Resolution, Categorization Tier 1, Categorization Tier 2, Categorization Tier 3, Product Categorization Tier 1, Product Categorization Tier 2, Product Categorization Tier 3, Resolution Category, Resolution Category Tier 2, Resolution Category Tier 3, Closure Product Category Tier1, Closure Product Category Tier2, Closure Product Category Tier3, Generic Categorization Tier 1, Generic Categorization Tier 2, Generic Categorization Tier 3)"
#GetIncDataUrl= BaseUrl + INC_Url + IncQueryQual + IncidentFieldList
GetIncDataUrl= BaseUrl+INC_Url+IncidentFieldList

# Incident WorkLog Query Parameters
#IncWOQueryQual = "?q=('Incident Number' = \"INC000000024397\")"
WorkLogFieldList = '?fields=values(Incident Number, Work Log ID, Description, Detailed Description)'
#GetIncWorkLogsUrl= BaseUrl+INC_WorkLogUrl+IncQueryQual+IncidentFieldList
GetIncWorkLogsUrl= BaseUrl + INC_WorkLogUrl + WorkLogFieldList

# Change Query Parameters
#CrqQueryQual = "?q='Change Infrastructure ID'=\"CRQ000000024397\""
CrqFieldList = "?fields=values(Infrastructure Change ID, Description, Detailed Description, Categorization Tier 1, Categorization Tier 2, Categorization Tier 3, Product Cat Tier 1, Product Cat Tier 2, Product Cat Tier 3)"
#GetCrqDataUrl= BaseUrl + INC_Url + IncQueryQual + IncidentFieldList
GetCrqUrl= BaseUrl+CRQ_Url+CrqFieldList

# Change WorkLog Query Parameters
#CrqWLQueryQual = "?q='Change Infrastructure ID'=\"CRQ000000024397\""
CrqWLFieldList = "?fields=values(Infrastructure Change ID, Work Log ID, Description, Detailed Description)"
#GetIncWorkLogsUrl= BaseUrl+INC_WorkLogUrl+IncQueryQual+IncidentFieldList
GetCrqWLUrl= BaseUrl + CRQ_WorkLogsUrl + CrqWLFieldList

# WorkOrder Query Parameters
# WoQueryQual = "?q='Work Order ID'=\"WO0000000024397\""
WoFieldList = "?fields=values(Work Order ID, Summary, Detailed Description,Categorization Tier 1, Categorization Tier 2, Categorization Tier 3, Product Categorization Tier 1, Product Categorization Tier 2, Product Categorization Tier 3)"
#GetWoDataUrl= BaseUrl + WO_Url + WOQueryQual + WoFieldList
GetWoUrl= BaseUrl+WO_Url+WoFieldList

# WorkOrder Work Logs Query Parameters
# WoWLQueryQual = "?q='Work Order ID'=\"WO0000000024397\""
WoWLFieldList = "?fields=values(Work Order ID, Work Log ID, Description, Detailed Description)"
#GetWoWLDataUrl= BaseUrl + WO_WorkLogsUrl + WOQueryQual + WoFieldList
GetWoWLUrl= BaseUrl+WO_WorkLogsUrl+WoWLFieldList

# Problem Query Parameters
# PbmQueryQual = "?q='Problem Investigation ID'=\"PBM000000024397\""
PbmFieldList = "?fields=values(Problem Investigation ID, Description, Detailed Decription, Temporary Workaround, Implemented Solution, Categorization Tier 1, Categorization Tier 2, Categorization Tier 3, Product Categorization Tier 1, Product Categorization Tier 2, Product Categorization Tier 3)"
#GetWoDataUrl= BaseUrl + PBM_Url + PbmQueryQual + WoFieldList
GetPbmUrl= BaseUrl+PBM_Url+PbmFieldList

# Problem WorkLog Query Parameters
# PbmWLQueryQual = "?q='Problem Investigation ID'=\"PBM000000024397\""
PbmWLFieldList = "?fields=values(Problem Investigation ID, Work Log ID, Description, Detailed Description)"
# GetPbmKEDataUrl= BaseUrl + PBM_WorkLogsUrl + PbmWLQueryQual + WoWLFieldList
GetPbmWLUrl= BaseUrl+PBM_WorkLogsUrl+PbmWLFieldList

# Known Error Query Parameters
# PbmKEQueryQual = "?q='Known Error ID'=\"PBM000000024397\""
PbmKEFieldList = "?fields=values(Known Error ID, Description, Detailed Decription, Temporary Workaround, Resolution, Categorization Tier 1, Categorization Tier 2, Categorization Tier 3, Product Categorization Tier 1, Product Categorization Tier 2, Product Categorization Tier 3, Generic Categorization Tier 1, Generic Categorization Tier 2, Generic Categorization Tier 3 )"
# GetPbmKEDataUrl= BaseUrl + PBM_Url + PbmQueryQual + WoFieldList
GetPbmKEUrl= BaseUrl+PBMKE_URL+PbmKEFieldList

# Known Error WorkLogs Query Parameters
# PbmKEWLQueryQual = "?q='Known Error ID'=\"PBM000000024397\""
PbmKEWLFieldList = "?fields=values(Known Error ID, Work Log ID, Description, Detailed Description)"
# GetPbmKEWLDataUrl= BaseUrl + PBMKE_WorkLog_URL + PbmQueryQual + WoFieldList
GetPbmKEWLUrl= BaseUrl+ PBMKE_WorkLog_URL +PbmKEWLFieldList

# Known Mgmt Query Parameters
# RkmQueryQual = "?q='Doc ID'=\"KM0000000024397\""
RkmFieldList = "?fields=values(DocID, Article_Keywords, Operational Categorization Tier 1, Operational Categorization Tier 2, Operational Categorization Tier 3, Product Categorization Tier 1, Product Categorization Tier 2, Product Categorization Tier 3, Resolution Categorization Tier 1, Resolution Categorization Tier 2, Resolution Categorization Tier 3, Closure Product Category Tier 1, Closure Product Category Tier 2, Closure Product Category Tier 3)"
# GetRkmDataUrl= BaseUrl + KM_Url + PbmQueryQual + RkmFieldList
GetRkmKEUrl= BaseUrl+KM_Url+RkmFieldList
