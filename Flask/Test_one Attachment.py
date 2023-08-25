import requests
from Auth import GetAuthToken as Auth

# Generate Helix Auth Token
helixToken= Auth()
methodheaders = {
        'Authorization': helixToken
}

print(methodheaders)
json_response = {
    "entries": [
        {
            "values": {
                "Work Order ID": "WO0000000021381",
                "z2AF Work Log01": {
                    "name": "Hi..Hello",
                    "sizeBytes": 79,
                    "href": "https://helixsjc814-demo-restapi.onbmc.com/api/arsys/v1/entry/WOI:WorkInfo/CWL000000000572/attach/z2AF%20Work%20Log01"
                }
            },
            "_links": {
                "self": [
                    {
                        "href": "https://helixsjc814-demo-restapi.onbmc.com/api/arsys/v1/entry/WOI:WorkInfo/CWL000000000572"
                    }
                ]
            }
        }
    ]
}

attachment_url = json_response["entries"][0]["values"]["z2AF Work Log01"]["href"]
attachment_name = json_response["entries"][0]["values"]["z2AF Work Log01"]["name"]
#print(attachment_url)
#print(attachment_name)
response = requests.get(attachment_url, headers=methodheaders)

if response.status_code == 200:
    print(response.text)
    print(f"Attachment '{attachment_name}' downloaded successfully.")
else:
    print("Failed to download attachment.")
