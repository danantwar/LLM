from bs4 import BeautifulSoup
import requests
import re
#import webLoad as web
import webLoadFunctions as wb
from werkzeug.utils import secure_filename
import os
import SQL_Functions as sq
import DataLoadLogging as logs
import validateDataLoad as val
import time
import threading

def dataLoadFromBMCKB(inputFile):
    totalrecords = 0
    # Get the file from the request
    file = inputFile   
    # Save the file to a temporary location
    filename = secure_filename(file.filename)
    temp_folder = 'C:\\Users\\jagadish.patil\\myTestEnv\\tempFiles'
    file.save(os.path.join(temp_folder, filename))
    file_path = os.path.join(temp_folder, filename)
    threading.Thread(target=processKBFile).start()
    httpResponse = "Data Load from BMC KB articles Initiated, check logs for more details."
    #totalrecords=processKBFile()
    return httpResponse
#--------------------------------------------------------------------------------------------------------------------------
def processKBFile():
    source = "BMC KB"
    loadHistoryResults = val.createLoadHistoryInDB(source)
    loadTimestamp = loadHistoryResults[0]
    loadStatus=loadHistoryResults[1]
    recordCount = 0
    start_time = time.time()

    # Define a regular expression pattern to match URLs
    url_pattern = r'https?://\S+'
    directory_path = 'C:\\Users\\jagadish.patil\\myTestEnv\\tempFiles'

    # List all files in the directory
    file_list = os.listdir(directory_path)

    # Loop through each file and read its content
    for filename in file_list:
        file_path = os.path.join(directory_path, filename)
        with open(file_path, 'r') as file:
            # Loop through each line in the file
            for line in file:
                # Use re.findall to find all URLs in the current line
                urls = re.findall(url_pattern, line)            
                for url in urls:
                    print(url)
                    dataExists = checkDataExists(url)   
                    if dataExists:
                        logs.writeLog(f"Data already exist in database for {url}, skipping the dataload for this Article.", "WARN")
                    else:
                        # Fetch the content of the URL using requests
                        try:
                            response = requests.get(url)
                            if response.status_code == 200:
                                page_content = response.text
                                recordCount+=processKBData(url, page_content)                    
                            else:
                                print(f"Failed to fetch URL: {url}, Status code: {response.status_code}")
                        except Exception as e:
                            print(f"Error fetching URL: {url}, Error: {e}")
    if loadStatus == "Running":
        loadStatus = "Completed"
        args = (loadStatus, source, loadTimestamp)
        val.updateLoadHistory(args)
    end_time = time.time()
    # Calculate the execution time
    execution_time = end_time - start_time
    logs.writeLog(f"Records loaded in database: {recordCount}", "INFO")
    logs.writeLog(f"DataLoad Finished in {execution_time:.6f} seconds.", "INFO")
    print(f"Execution Time: {execution_time:.6f} seconds.")
    return recordCount
#--------------------------------------------------------------------------------------------------------------------------
def checkDataExists(url):
    conn = sq.getconnection()
    query = "SELECT content FROM public.\"LLM\" WHERE reference = '" + url + "'"

    try:
        cursor = conn.cursor()        
        cursor.execute(query)
        records = cursor.fetchall()
        if records:
            dataExists = True
        else:
            dataExists = False
    except (Exception) as error:
        print("Error while reading records:", error)
  
    conn.close()
    return dataExists
#-----------------------------------------------------------------
def processKBData(url, page_source):
# Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

# Find all the div elements with class "action-detail"
    action_details = soup.find_all("div", class_="action-detail")

# Initialize a dictionary to store labels and values
    label_value_dict = {}

# Iterate through each "action-detail" div
    for action_detail in action_details:
        # Find the label text within the "action-label" div
        label = action_detail.find("div", class_="action-label").text.strip()

        # Find the value within the "action-value" div
        value = action_detail.find("div", class_="action-value").text.strip()

        # Add the label and value to the dictionary
        label_value_dict[label] = value

# extracte labels and values and load into DB
    content=""
    contentMetaData=""
    for label, value in label_value_dict.items():
        #print(f"{label}: {value}")
        contentMetaData = contentMetaData + (f"{label}: {value}" +"\n")
        content= content +" "+ value
    source = "BMC KB"
    recordCount=wb.loadKBDataInDB(source, url, content, contentMetaData)
    return recordCount
#-----------------------------------------------------------------