# app.py
from flask import Flask, render_template, request, jsonify
import DataLoadLogging as logs
import helixLoadFunctions as helix
import threading
import validateDataLoad as val
import webLoadFunctions as wb
import fileLoadFunctions as fileload
import bulkFileLoad as bf
import loadArtilcesFromFile as kbload
import bulkFileLoad as bf

#--------------------------------------------------------------------------------------------------------------------------

app = Flask(__name__)

#--------------------------------------------------------------------------------------------------------------------------
# ------- Following def main() function will be triggered for cals received from WebApp ------------------------------------
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
        
        if Source =="KB":
            kbFile = request.files['KBLoad']
            loadResponse = kbload.dataLoadFromKB(kbFile)            
            return render_template('index.html', response=loadResponse)
        
        if Source =="FILE":
            dataFile = request.files['FileUpload']
            loadResponse = fileload.dataLoadFromFile(dataFile)
            return render_template('index.html', response=loadResponse)
        if Source =="BULKFILE":
            loadResponse = bf.startBulkLoad()
            return render_template('index.html', response=loadResponse)
        if Source == "WEB":
            url = request.form['Web_URL']
            loadResponse = wb.loadFromWeb(url)
            return render_template('index.html', response=loadResponse)

    return render_template('index.html')

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
@app.post("/load/kb")
def loadFromKB():
    if request.form:
        kbFile =  request.form['KBLoad']        
        httpResponse =  kbload.dataLoadFromKB(kbFile)  
        return httpResponse
    else:
        httpResponse = {"error": "Text file with KB URLs is required for this type of data load."}
        httpCode = 415
        response = jsonify(httpResponse)
        response.status_code = httpCode
        return response
#---------------------------------------------------------------------------------------------------------------------------------------
@app.post("/load/file")
def loadFromFile():
    if request.form:
        dataFile =  request.form['fileUpload']
        httpResponse = fileload.dataLoadFromFile(dataFile)
        return httpResponse
    else:
        httpResponse = {"error": "Data File is required for this type of data load."}
        httpCode = 415
        response = jsonify(httpResponse)
        response.status_code = httpCode
        return response

@app.post("/load/bulkfile")
def loadBulkFile():
    source = "BULKFILELOAD"
    initiateLoad = val.validateLoad(source)
    if initiateLoad:
        threading.Thread(target=bf.loadFileInBulk).start()
        httpResponse = {"message": "Bulk File Data Load is Initiated"}
        httpCode = 202
        response = jsonify(httpResponse)
        response.status_code = httpCode
        return response
    else:
        logs.writeLog(f"Previous Bulk File Data Load not completed yet, wait for previous load completion.", "ERROR")
        logs.writeLog("Data Load Terminated.", "ERROR")
        httpResponse = "Previous Bulk File Data Load not completed yet, wait for previous load completion."
        httpCode = 415
        response = httpResponse
        response = jsonify(httpResponse)
        response.status_code = httpCode
        return response


@app.post("/load/web")
def loadFromWeb():
    if request.is_json:
        payload = request.get_json()   
        url =  payload["WebURL"]
        dataExists = wb.checkDataExists(url)
        if dataExists:
            logs.writeLog(f"Data already exist in database for {url} , please try data load for any other URL.", "ERROR")
            logs.writeLog("Data Load Terminated.", "ERROR")
            httpResponse = {"error" : f"Data already exist in database for {url} , please try data load for any other URL."}
            httpCode = 415
        else:
            logs.writeLog(f"Data Load Initiated from website URL: {url}", "INFO")      
            wbResponse = wb.loadWebData(url)
            if wbResponse > 0:
                httpResponse = {"message" : f"Data Loaded from URL:{url} successfully. Total {wbResponse} records created in database."}
                httpCode = 202
            else:
                httpResponse = {"message" : f"Data Load from URL:{url} has failed, please check logs for more details."}
                httpCode = 500    
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

if __name__ == '__main__':
    app.run(debug=False)
