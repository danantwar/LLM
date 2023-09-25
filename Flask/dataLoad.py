import helixLoad as helix
import webLoad as web
import fileLoad as file
import DataLoadLogging as logs
from flask import jsonify

def fullDataLoadFromHelix():
    logs.writeLog("Full Data Load from Helix requested via API.", "INFO")
    loadType = "FULL"
    response = helix.initiateHelixLoad(loadType)
    httpResponse = response[0]
    httpCode = response[1]

    #   apiResponse = {"message": httpResponse}
    response = jsonify(httpResponse)
    response.status_code = httpCode
    return response
#---------------------------------------------------------------------------------

def deltaDataLoadFromHelix():
    logs.writeLog("Delta Data Load from Helix requested via API.", "INFO")
    loadType = "DELTA"
    helixResponse = helix.initiateHelixLoad(loadType)
    httpResponse = helixResponse[0]
    httpCode = helixResponse[1]

    #   apiResponse = {"message": httpResponse}
    response = jsonify(httpResponse)
    response.status_code = httpCode
    return response
#-----------------------------------------------------------------------------------
def dataLoadFromWeb(url):    
    httpResponse = ""
    httpCode = 0
    if url.startswith("http://") or url.startswith("https://"):
        logs.writeLog("Data Load from Web URL requested via API.", "INFO")
        httpResponse = {"message": "Data Load from provided URL is initiated, check logs for more details."}
        httpCode = 202
        web.loadWebData(url)
    else:
        httpResponse = {"error": "URL value is mandatory for Web Data Load."}
        httpCode = 500
        logs.writeLog("URL value is missing from request for Web Data Load.", "ERROR")
        logs.writeLog("Data Load Terminated.", "ERROR")

    #   apiResponse = {"message": httpResponse}
    response = jsonify(httpResponse)
    response.status_code = httpCode
    return response
#-----------------------------------------------------------------------------------
def dataLoadFromBMCKB(kbFile):
    httpResponse = ""
    httpCode = 0
    if len(kbFile) != 0:
        logs.writeLog("Data Load from BMC KB Articles using provided URLs in file has requested via API.", "INFO")
        kbResponse = file.loadFromFile(kbFile)
        httpResponse = kbResponse[0]
        httpCode = kbResponse[1]
    else:
        httpResponse = {"error": "Provided file does not contain any URLs Data Load."}
        httpCode = 500
        logs.writeLog("BMC KB URLs are missing in provided file for Data Load.", "ERROR")
        logs.writeLog("Data Load Terminated.", "ERROR")
    #   apiResponse = {"message": httpResponse}
    response = jsonify(httpResponse)
    response.status_code = httpCode
    return response
#-----------------------------------------------------------------------------------
def dataLoadFromFile(dataFile):
    httpResponse = ""
    httpCode = 0
    if len(dataFile) != 0:
        logs.writeLog("Data Load from provided data file has requested via API.", "INFO")
        fileResponse = file.loadFromFile(dataFile)
        httpResponse = fileResponse[0]
        httpCode = fileResponse[1]
    else:
        httpResponse = {"error": "Provided fiel does not contian any URLs Data Load."}
        httpCode = 500
        logs.writeLog("BMC KB URLs are missing in provided file for Data Load.", "ERROR")
        logs.writeLog("Data Load Terminated.", "ERROR")
    #   apiResponse = {"message": httpResponse}
    response = jsonify(httpResponse)
    response.status_code = httpCode
    return response
#-----------------------------------------------------------------------------------