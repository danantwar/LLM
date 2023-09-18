# app.py
from flask import Flask, render_template, request
import helixLoad as helix
import webLoad as web
import fileLoad as file

app = Flask(__name__)


@app.post("/load")
def loadData():
    if request.is_json:
        payload = request.get_json()
        source = payload["source"]  
        
        if source == "HELIX":            
            loadType = payload["loadType"]
            if loadType == "FULL" or loadType == "DELTA":
                helix.initiateHelixLoad(loadType)
            else:
                return {"error": "LoadType value is not correct for Helix Data Laod."}, 415                 
                
        if source == "WEB":
            url =  payload["url"]
            if url.startswith("http://") or url.startswith("https://"):
                web.loadWebData(url)                
            else:
                return {"error": "URL value is manadatory for Web Data Load."}, 415 
                

    elif request.form:
        source = request.form['source']
        if source == "FILE":
            dataFile =  request.form['file']
            if len(dataFile) != 0:
                file.loadFromFile(dataFile)
            else:
                return {"error": "Data Load File Content are manadatory for File Data Laod."}, 415 
                                
    return {"response": "Data Load Request Recevied"}, 200  
    

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        Source = request.form['LoadSource']
        LoadType = request.form['HelixLoadType']
        response = ""
                
        if Source =="HELIX" and LoadType !="" :
            loadResponse = helix.initiateHelixLoad(LoadType)            
            return render_template('index.html', response=loadResponse)
        
        if Source =="FILE":
            print("I am on file")
            inputFile = request.files['Attachment']
            loadResponse = file.loadFromFile(inputFile)
            
            return render_template('index.html', response=loadResponse)
            
        if Source == "WEB":
            WebURL = request.form['WebURL']
            print("I am on Web Page")
            print(WebURL)
            loadResponse = web.loadWebData(WebURL)
            return render_template('index.html', response=loadResponse)
            
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)