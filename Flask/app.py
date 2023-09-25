# app.py
from flask import Flask, render_template, request, jsonify
import DataLoadLogging as logs
import dataLoad as load

app = Flask(__name__)


#------- Following Functions will be triggered by REST API Calls ----------------------------#
@app.post("/load")
def loadData():
    httpResponse = {"error": """You must provide the type of load in URL.
                    refer examples:
                    /load/helix/full
                    /load/helix/delta
                    /load/bmckb
                    /load/web
                    /load/file"""
                    }
    httpCode = 415
    logs.writeLog("Load URL is incorrect, kindly provide correct app context.", "ERROR")#   apiResponse = {"message": httpResponse}
    response = jsonify(httpResponse)
    response.status_code = httpCode
    return response    

@app.post("/load/helix/full")
def loadFromHelixFull():
    httpResponse = load.fullDataLoadFromHelix()
    return httpResponse

@app.post("/load/helix/delta")
def loadFromHelixDelta():
    httpResponse = load.deltaDataLoadFromHelix()
    return httpResponse

@app.post("/load/bmckb")
def loadFromBMCKB():
    if request.form:
        kbFile =  request.form['KBLoad']
        httpResponse = load.dataLoadFromBMCKB(kbFile)
        return httpResponse
    else:
        httpResponse = {"error": "Text file with BMC KB URLs is required for this type of data load."}
        httpCode = 415
        response = jsonify(httpResponse)
        response.status_code = httpCode
        return response

@app.post("/load/file")
def loadFromFile():
    if request.form:
        dataFile =  request.form['fileUpload']
        httpResponse = load.dataLoadFromFile(dataFile)
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
        httpResponse = load.dataLoadFromWeb(url)
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

if __name__ == '__main__':
    app.run(debug=False)


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        Source = request.form['LoadSource']
        LoadType = request.form['HelixLoadType']
        loadResponse = ""
                
        if Source =="HELIX" and LoadType =="FULL" :
            loadResponse = load.fullDataLoadFromHelix()
            return render_template('index.html', response=loadResponse)
        
        if Source =="HELIX" and LoadType =="DELTA" :
            loadResponse = load.deltaDataLoadFromHelix()
            return render_template('index.html', response=loadResponse)
        
        if Source =="BMC KB":
            kbFile = request.files['kbLoad']
            loadResponse = load.dataLoadFromBMCKB(kbFile)            
            return render_template('index.html', response=loadResponse)
        
        if Source =="FILE":
            dataFile = request.files['fileUpload']
            loadResponse = load.dataLoadFromFile(dataFile)
            return render_template('index.html', response=loadResponse)
            
        if Source == "WEB":
            url = request.form['WebURL']
            loadResponse = load.dataLoadFromWeb(url)
            return render_template('index.html', response=loadResponse)
            
    return render_template('index.html')