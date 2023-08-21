# API endpoint URL

BaseUrl = 'https://helixsjc814-demo-restapi.onbmc.com'
username = 'Seth'
password = 'Password_1234'
AuthUrl = '/api/jwt/login'
IncidentsUrl = '/api/arsys/v1/entry/HPD:Help Desk'
IncidentWorkLogUrl = '/api/arsys/v1/entry/HPD:WorkLog'

QueryQual = "?q=('Status' = \"Resolved\")"
IncidentFieldList = '&fields=values(Incident Number, Description, Status)'
GetIncidentsUrl= BaseUrl+IncidentsUrl+QueryQual+IncidentFieldList


