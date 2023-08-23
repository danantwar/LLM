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
WO_Url = 'WOI:WorkOrder'
WO_WorkLogsUrl = 'WOI:WorkInfo'
KM_Url = 'RKM:KNowledgeArticleManager'

# Incident Query Parameters
QueryQual = "?q=('Incident Number' = \"INC000000024397\")"
IncidentFieldList = '&fields=values(Incident Number, Description, Detailed Decription,Resolution, Categorization Tier 1, Categorization Tier 2, Categorization Tier 3, Product Categorization Tier 1, Product Categorization Tier 2, Product Categorization Tier 3, Resolution Category, Resolution Category Tier 2, Resolution Category Tier 3, Closure Product Category Tier1, Closure Product Category Tier2, Closure Product Category Tier3, Generic Categorization Tier 1, Generic Categorization Tier 2, Generic Categorization Tier 3)'
GetIncDataUrl= BaseUrl+INC_Url+QueryQual+IncidentFieldList
#GetIncDataUrl= BaseUrl+INC_Url+IncidentFieldList

# Incident WorkLog Query Parameters
#QueryQual = "?q=('Status' = \"Resolved\")"
WorkLogFieldList = '&fields=values(Incident Number, Work Log ID, Description, Detailed Decription)'
#GetIncWorkLogsUrl= BaseUrl+INC_WorkLogUrl+QueryQual+IncidentFieldList
GetIncWorkLogsUrl= BaseUrl+INC_WorkLogUrl+WorkLogFieldList
