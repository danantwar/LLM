import logging as log
import datetime

def writeLog(logEntry, logLevel):
 # Configure the logging module
 
 log.basicConfig(filename='logs\execution.log', level=log.DEBUG,
                    format='%(asctime)s - %(levelname)s: %(message)s')
 
 if logLevel == "INFO":
       log.info(logEntry)
 elif logLevel == "WARN":
       log.warning(logEntry)
 elif logLevel == "ERROR":
       log.error(logEntry)

# writeLog("Test writing in log file.", "INFO")
# writeLog("Test writing in log file.", "WARN")
# writeLog("Test writing in log file.", "ERROR")