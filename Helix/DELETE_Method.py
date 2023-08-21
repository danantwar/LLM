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

#use token in for DELETE method, Create Inciden
methodUrl='https://helixsjc814-demo-restapi.onbmc.com/api/arsys/v1/entry/HPD:Help Desk/INC000000003497'
methodheaders = {
        'Authorization': myAccessToken,
}

methodresponse = requests.delete(methodUrl, headers=methodheaders)

print(methodresponse.status_code)
