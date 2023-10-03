# app.py
from flask import Flask, render_template, request, jsonify
import DataLoadLogging as logs
import helixLoadFunctions as helix
import threading
import validateDataLoad as val

app = Flask(__name__)

#------- Following Functions will be triggered by REST API Calls ----------------------------#
@app.post("/load")
def loadData():
    httpResponse = {"error": """You must provide the type of load in URL.
                    refer examples: /load/helix/full  /load/helix/delta /load/bmckb  /load/web /load/file"""
                    }
    httpCode = 415
    logs.writeLog("Load URL is incorrect, kindly provide correct app context.", "ERROR")#   apiResponse = {"message": httpResponse}
    response = jsonify(httpResponse)
    response.status_code = httpCode
    return response    
#---------------------------------------------------------------------------------------------------------------------------------------
@app.post("/load/helix/full")
def loadFromHelixFull():
    source = "HELIX"
    initiateLoad = val.validateLoad(source)
    if initiateLoad:
        logs.writeLog(f"Full Data Load Initiated for Data Source:{source}.", "INFO")      
        threading.Thread(target=helix.helixLoadFull).start()
        httpResponse = {"message" : f"Full Data Load Initiated from source: {source}, check logs for more details."}
        httpCode = 202
    else:
        logs.writeLog(f"Previous DataLoad from source: {source} not completed yet, wait for previous load completion.", "ERROR")
        logs.writeLog("Data Load Terminated.", "ERROR")
        httpResponse = {"error" : f"Previous DataLoad from source: {source} not completed yet, wait for previous load completion."}
        httpCode = 415

    response = jsonify(httpResponse)
    response.status_code = httpCode
    return response
#---------------------------------------------------------------------------------------------------------------------------------------
@app.post("/load/helix/delta")
def loadHelixDataDelta():
    source = "HELIX"
    initiateLoad = val.validateLoad(source)
    if initiateLoad:
        logs.writeLog(f"Delta Data Load Initiated for Data Source:{source}.", "INFO")      
        threading.Thread(target=helix.helixLoadDelta).start()
        httpResponse = {"message" : f"Delta Data Load Initiated from source: {source}, check logs for more details."}
        httpCode = 202
    else:
        logs.writeLog(f"Previous DataLoad from source: {source} not completed yet, wait for previous load completion.", "ERROR")
        logs.writeLog("Data Load Terminated.", "ERROR")
        httpResponse = {"error" : f"Previous DataLoad from source: {source} not completed yet, wait for previous load completion."}
        httpCode = 415

    response = jsonify(httpResponse)
    response.status_code = httpCode
    return response
#---------------------------------------------------------------------------------------------------------------------------------------
@app.post("/load/bmckb")
def loadFromBMCKB():
    if request.form:
        kbFile =  request.form['KBLoad']
#        httpResponse = load.dataLoadFromBMCKB(kbFile)
        return httpResponse
    else:
        httpResponse = {"error": "Text file with BMC KB URLs is required for this type of data load."}
        httpCode = 415
        response = jsonify(httpResponse)
        response.status_code = httpCode
        return response
#---------------------------------------------------------------------------------------------------------------------------------------
@app.post("/load/file")
def loadFromFile():
    if request.form:
        dataFile =  request.form['fileUpload']
#        httpResponse = load.dataLoadFromFile(dataFile)
        return httpResponse
    else:
        httpResponse = {"error": "Data File is required for this type of data load."}
        httpCode = 415
        response = jsonify(httpResponse)
        response.status_code = httpCode
        return response

@app.post("/load/web")
def loadFromWeb():
    if request.is_json:
        payload = request.get_json()   
        url =  payload["url"]
 #       httpResponse = load.dataLoadFromWeb(url)
        return httpResponse
    else:
        httpResponse = {"error": """Request json is required with a URL value for this type of data load.
                                    Example json:
                                    {
                                        "url" : "https://en.wikipedia.org/wiki/Fusion_Global_Business_Solutions"
                                    }
                        """}
        httpCode = 415
        response = jsonify(httpResponse)
        response.status_code = httpCode
        return response
#--------------------------------------------------------------------------------------------------------------------------

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        Source = request.form['LoadSource']
        LoadType = request.form['HelixLoadType']
        loadResponse = ""
                
        if Source =="HELIX" and LoadType =="FULL" :
            loadResponse = helix.loadFromHelixFull()
            return render_template('index.html', response=loadResponse)
        
        if Source =="HELIX" and LoadType =="DELTA" :
            loadResponse = helix.loadHelixDataDelta()

            return render_template('index.html', response=loadResponse)
        
        if Source =="BMC KB":
            kbFile = request.files['kbLoad']
#            loadResponse = load.dataLoadFromBMCKB(kbFile)            
#            return render_template('index.html', response=loadResponse)
        
        if Source =="FILE":
            dataFile = request.files['fileUpload']
#            loadResponse = load.dataLoadFromFile(dataFile)
#            return render_template('index.html', response=loadResponse)
            
        if Source == "WEB":
            url = request.form['WebURL']
#           loadResponse = load.dataLoadFromWeb(url)
#            return render_template('index.html', response=loadResponse)
            
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)
