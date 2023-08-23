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
#IncQueryQual = "?q='Incident Number'=\"INC000000024397\""
IncidentFieldList = "?fields=values(Incident Number, Description, Detailed Decription,Resolution, Categorization Tier 1, Categorization Tier 2, Categorization Tier 3, Product Categorization Tier 1, Product Categorization Tier 2, Product Categorization Tier 3, Resolution Category, Resolution Category Tier 2, Resolution Category Tier 3, Closure Product Category Tier1, Closure Product Category Tier2, Closure Product Category Tier3, Generic Categorization Tier 1, Generic Categorization Tier 2, Generic Categorization Tier 3)"
#GetIncDataUrl= BaseUrl + INC_Url + IncQueryQual + IncidentFieldList
GetIncDataUrl= BaseUrl+INC_Url+IncidentFieldList

# Incident WorkLog Query Parameters
#IncWOQueryQual = "?q=('Incident Number' = \"INC000000024397\")"
WorkLogFieldList = '?fields=values(Incident Number, Work Log ID, Description, Detailed Description)'
#GetIncWorkLogsUrl= BaseUrl+INC_WorkLogUrl+IncQueryQual+IncidentFieldList
GetIncWorkLogsUrl= BaseUrl + INC_WorkLogUrl + WorkLogFieldList

# Incident Query Parameters
#IncQueryQual = "?q='Incident Number'=\"INC000000024397\""
IncFieldList = "?fields=values(Incident Number, Description, Detailed Decription,Resolution, Categorization Tier 1, Categorization Tier 2, Categorization Tier 3, Product Categorization Tier 1, Product Categorization Tier 2, Product Categorization Tier 3, Resolution Category, Resolution Category Tier 2, Resolution Category Tier 3, Closure Product Category Tier1, Closure Product Category Tier2, Closure Product Category Tier3, Generic Categorization Tier 1, Generic Categorization Tier 2, Generic Categorization Tier 3)"
#GetIncDataUrl= BaseUrl + INC_Url + IncQueryQual + IncidentFieldList
GetIncUrl= BaseUrl+INC_Url+IncFieldList

# Incident WorkLog Query Parameters
#IncWLQueryQual = "?q=('Incident Number' = \"INC000000024397\")"
IncWLFieldList = '?fields=values(Incident Number, Work Log ID, Description, Detailed Description)'
#GetIncWLUrl= BaseUrl+INC_WorkLogUrl+IncQueryQual+IncidentFieldList
GetIncWLUrl= BaseUrl + INC_WorkLogUrl + IncWLFieldList

# Change Query Parameters
#CrqQueryQual = "?q='Change Infrastructure ID'=\"CRQ000000024397\""
CrqFieldList = "?fields=values(Incident Number, Description, Detailed Decription,Resolution, Categorization Tier 1, Categorization Tier 2, Categorization Tier 3, Product Categorization Tier 1, Product Categorization Tier 2, Product Categorization Tier 3, Resolution Category, Resolution Category Tier 2, Resolution Category Tier 3, Closure Product Category Tier1, Closure Product Category Tier2, Closure Product Category Tier3, Generic Categorization Tier 1, Generic Categorization Tier 2, Generic Categorization Tier 3)"
#GetCrqDataUrl= BaseUrl + INC_Url + IncQueryQual + IncidentFieldList
GetCrqUrl= BaseUrl+CRQ_Url+CrqFieldList

# Change WorkLog Query Parameters
#CrqWLQueryQual = "?q='Change Infrastructure ID'=\"CRQ000000024397\""
CrqWLFieldList = '?fields=values(Incident Number, Work Log ID, Description, Detailed Description)'
#GetIncWorkLogsUrl= BaseUrl+INC_WorkLogUrl+IncQueryQual+IncidentFieldList
GetIncWLUrl= BaseUrl + CRQ_WorkLogsUrl + CrqWLFieldList
