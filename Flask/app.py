# app.py
from flask import Flask, render_template, request, jsonify
import helixLoad as helix
import webLoad as web
import fileLoad as file
import threading
import SQL_Functions as sq
import DataLoadLogging as logs

app = Flask(__name__)

def initiateHelixLoad(LoadType):    
    source = "HELIX"    
    loadHistoryResults = sq.getLastLoadTimestamp(source)     
    lastLoadTimestamp = loadHistoryResults[0]
    loadStatus=loadHistoryResults[1]
    print("Last Load Status: ", loadStatus)
    if (loadStatus == "Completed" or loadStatus == ""):
        initiateLoad = True
    else:
        initiateLoad = False
        
    if initiateLoad:
        args = (initiateLoad, source, LoadType)
        thread = threading.Thread(target=helix.helixLoad(args))
        thread.start()
        logs.writeLog(f"DataLoad Initiated for Data Source:{source}.", "INFO")
        httpResponse = {"message" : f"DataLoad Initiated for {source}, check logs for more details."}
        httpCode = 202
    else:
        httpResponse = {"error" : f"Previous DataLoad for {source} has not completed yet, wait for previous load completion."}
        httpCode = 415
        logs.writeLog(f"Previous DataLoad for {source} has not completed yet, wait for previous load completion.", "WARN")
        logs.writeLog("Data Load Terminated.", "ERROR")
    
    return httpResponse, httpCode

@app.post("/load")
def loadData():
    logs.writeLog("Data Load API Request Received.", "INFO")
    httpResponse = ""
    httpCode = 0
    if request.is_json:
        payload = request.get_json()
        source = payload["source"]  
        
        if source == "HELIX" or source == "WEB":
            if source == "HELIX":            
                loadType = payload["loadType"]
                if loadType == "FULL" or loadType == "DELTA":
                    #loadResponse = helix.initiateHelixLoad(loadType)
                    response = initiateHelixLoad(loadType)        
                    httpResponse = response[0]
                    httpCode = response[1]
                else:
                    httpResponse = {"error": "LoadType value is not correct for Helix Data Load."}
                    httpCode = 415
                    logs.writeLog("LoadType value is not correct for Helix Data Load.", "ERROR")
                    logs.writeLog("Data Load Terminated.", "ERROR")
            if source == "WEB":
                url =  payload["url"]
                if url.startswith("http://") or url.startswith("https://"):
                    web.loadWebData(url)                
                else:
                    httpResponse = {"error": "URL value is mandatory for Web Data Load."}
                    httpCode = 415
                    logs.writeLog("URL value is mandatory for Web Data Load.", "ERROR")
                    logs.writeLog("Data Load Terminated.", "ERROR")
        else:
            httpResponse = {"error": "Source value is not valid, kindly provide correct source value."}
            httpCode = 415
            logs.writeLog("Source value is not valid, kindly provide correct source value.", "ERROR")
            logs.writeLog("Data Load Terminated.", "ERROR")
            
    elif request.form:
        source = request.form['source']
        if source == "FILE" or source == "BMC KB":
            if source == "FILE":
                dataFile =  request.form['FileUpload']
                if len(dataFile) != 0:
                    file.loadFromFile(dataFile)
                else:
                    httpResponse = {"error": "Data File with contents is mandatory for Data Load using File."}
                    httpCode = 415
                    logs.writeLog("Data File with contents is mandatory for Data Load using File.", "ERROR")
                    logs.writeLog("Data Load Terminated.", "ERROR")

            if source == "BMC KB":
                dataFile =  request.form['KBLoad']
                if len(dataFile) != 0:
                    file.loadFromFile(dataFile)
                else:
                    httpResponse = {"error": "Data Load File Content are manadatory for File Data Laod."}
                    httpCode = 415
                    logs.writeLog("File with BMC KB URLs is mandatory for BMC KB Data Load.", "ERROR")
                    logs.writeLog("Data Load Terminated.", "ERROR")
        else:
            httpResponse = {"error": "Source value is not valid, kindly provide correct source value."}
            httpCode = 415
            logs.writeLog("Source value is not valid, kindly provide correct source value.", "ERROR")
            logs.writeLog("Data Load Terminated.", "ERROR")

    
#   apiResponse = {"message": httpResponse}
    response = jsonify(httpResponse)
    response.status_code = httpCode
    return response


if __name__ == '__main__':
    app.run(debug=False)


'''
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        Source = request.form['LoadSource']
        LoadType = request.form['HelixLoadType']
        response = ""
                
        if Source =="HELIX" and LoadType !="" :
            loadResponse = initiateHelixLoad(LoadType)            
            return render_template('index.html', response=loadResponse)
        
        if Source =="FILE":
            print("I am on file")
            inputFile = request.files['Attachment']
            loadResponse = file.loadFromFile(inputFile)
            
            return render_template('index.html', response=loadResponse)
            
        if Source == "WEB":
            WebURL = request.form['WebURL']
            #print("I am on Web Page")
            #print(WebURL)
            loadResponse = web.loadWebData(WebURL)
            return render_template('index.html', response=loadResponse)
            
    return render_template('index.html')
'''