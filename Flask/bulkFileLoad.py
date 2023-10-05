import os
import fileReadFunctions as frf
import fileLoadFunctions as fl
import configs as conf
import validateDataLoad as val
import DataLoadLogging as logs
import time
import shutil
import threading

def startBulkLoad():
    source = "BULKFILELOAD"
    initiateLoad = val.validateLoad(source)
    if initiateLoad:
        threading.Thread(target=loadFileInBulk).start()
        httpResponse = "Bulk File Data Load is Initiated."
        return httpResponse
    else:
        logs.writeLog(f"Previous Bulk File Data Load not completed yet, wait for previous load completion.", "ERROR")
        logs.writeLog("Data Load Terminated.", "ERROR")
        httpResponse = "Previous Bulk File Data Load not completed yet, wait for previous load completion."
        return httpResponse

def loadFileInBulk():
    #Initialize Variables
    source = "BULKFILELOAD"    
    # Define the directory path where your files are located
    directory_path = conf.dataFile_dir
    archive_path = conf.archive_dir
    
    # List all files in the directory
    file_list = os.listdir(directory_path)
    if bool(file_list):
        loadHistoryResults = val.createLoadHistoryInDB(source)
        loadTimestamp = loadHistoryResults[0]
        loadStatus=loadHistoryResults[1]
        recordCount = 0
        start_time = time.time()

        # Loop through each file and read its content
        for filename in file_list:
            dataExists = fl.checkDataExists(filename)
            file_path = os.path.join(directory_path, filename)
            if not dataExists:
                # Check if the file is a regular file (not a directory)
                if os.path.isfile(file_path):           
                    file_content = frf.read_file_content(file_path)
                    file_content = file_content.replace('\r', '').replace('\n', '')
                    #file_content = file_content.replace('\xa0', ' ')
                    # Load content in database
                    recordCount += fl.loadDataInDB (source, filename, file_content)
            else:
                logs.writeLog(f"Data already exist in database for {filename} , skipping this file.", "WARN")

            destination_path = os.path.join(archive_path, os.path.basename(filename))
            if os.path.exists(destination_path):
                os.remove(destination_path) 
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
    else:
        logs.writeLog(f"No files found in configured directory: {directory_path} for bulk data load.", "WARN")
    


        
