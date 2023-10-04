import os
import fileReadFunctions as frf
import fileLoadFunctions as fl
import configs as conf
import validateDataLoad as val
import DataLoadLogging as logs
import time
import shutil

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
            shutil.move(file_path, archive_path)
    else:
        logs.writeLog(f"No files found in configured directory: {directory_path} for bulk data load.")
    
    if loadStatus == "Running":
        loadStatus = "Completed"
        args = (loadStatus, source, loadTimestamp)
        val.updateLoadHistory(args)
    end_time = time.time()
    # Calculate the execution time
    execution_time = end_time - start_time
    logs.writeLog(f"Records loaded in database: {recordCount}", "INFO")
    logs.writeLog(f"DataLoad Finished in {execution_time:.6f} seconds.", "INFO")
    print(f"Records loaded in database: {recordCount}")
    print(f"DataLoad Finished in {execution_time:.6f} seconds.")

        
