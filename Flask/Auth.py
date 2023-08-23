import configs
import requests
 
# Create operation
def GetAuthToken():
# API endpoint URL
 tokenurl = configs.AuthUrl
# Form data to be sent
 tokendata = {
    'username': configs.username,
    'password': configs.password
 }

# Send POST request with x-www-form-urlencoded data
 response = requests.post(tokenurl, data=tokendata)

# Print the response
 helixToken="AR-JWT "+response.text
 #print(helixToken)
 
#GetAuthToken() 
 return helixToken