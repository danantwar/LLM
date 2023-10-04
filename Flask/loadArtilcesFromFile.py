from bs4 import BeautifulSoup
import requests
import re
from werkzeug.utils import secure_filename
import os
import time
import threading
import shutil
import webLoadFunctions as wb
import SQL_Functions as sq
import DataLoadLogging as logs
import validateDataLoad as val
import configs as conf

def dataLoadFromKB(inputFile):
    #Initialize variables
    directory_path = conf.dataFile_dir
    # Get the file from the request
    file = inputFile   
    # Save the file to a temporary location
    filename = secure_filename(file.filename)
    file_ext = filename.split('.')
    isText = (file_ext[1]== "txt")
    file.save(os.path.join(directory_path, filename))
    file_path = os.path.join(directory_path, filename)
    file_size = os.path.getsize(file_path)
    
    if file_size > 0 or isText:    
        threading.Thread(target=processKBFile).start()
        httpResponse = "Data Load from KB articles Initiated, check logs for more details."
    else:
        httpResponse = "Invalid file for Data Load from KB articles, Kindly provide valid .txt file consists of KB URLs."
    return httpResponse
#--------------------------------------------------------------------------------------------------------------------------
def processKBFile():
    source = "KB"
    loadHistoryResults = val.createLoadHistoryInDB(source)
    loadTimestamp = loadHistoryResults[0]
    loadStatus=loadHistoryResults[1]
    recordCount = 0
    start_time = time.time()

    # Define a regular expression pattern to match URLs
    url_pattern = r'https?://\S+'
    directory_path = conf.KB_dir
    archive_path = conf.archive_dir
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
        shutil.move(file_path, archive_path)          
    if loadStatus == "Running":
        loadStatus = "Completed"
        args = (loadStatus, source, loadTimestamp)
        val.updateLoadHistory(args)
    end_time = time.time()
    # Calculate the execution time
    execution_time = end_time - start_time
    logs.writeLog(f"Records loaded in database: {recordCount}", "INFO")
    logs.writeLog(f"DataLoad Finished in {execution_time:.6f} seconds.", "INFO")
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
    source = "KB"
    recordCount=wb.loadKBDataInDB(source, url, content, contentMetaData)
    return recordCount
#-----------------------------------------------------------------