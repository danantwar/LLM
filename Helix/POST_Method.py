import requests

# API endpoint URL
tokenurl = 'https://helixsjc814-demo-restapi.onbmc.com/api/jwt/login'

# Form data to be sent
tokendata = {
    'username': 'Seth',
    'password': 'Password_1234'
}

# Send POST request with x-www-form-urlencoded data
response = requests.post(tokenurl, data=tokendata)

# Print the response
myAccessToken="AR-JWT "+response.text
#print(myAccessToken)

#use token in for POST method, Create Inciden
methodUrl='https://helixsjc814-demo-restapi.onbmc.com/api/arsys/v1/entry/HPD:IncidentInterface_Create?fields=values(Incident Number,Status)'
methodheaders = {
        'Authorization': myAccessToken,
        'Content-Type': 'application/json'
}
methoddata =  {
    "values": {
        "z1D_Action": "CREATE",
        "Login_ID": "Seth",
        "Description": "Test Incident from Python",
        "Detailed_Decription": "Test Incident from Python",
        "Impact": "3-Moderate/Limited",
        "Urgency": "3-Medium",
        "Reported Source": "Web",
        "Service_Type": "User Service Request",
        "Assigned Support Company": "Apex Global",
        "Assigned Group": "CD Pipeline",
        "Assigned Support Organization": "Development"
    }
}

methodresponse = requests.post(methodUrl, json=methoddata, headers=methodheaders)

print(methodresponse.status)

