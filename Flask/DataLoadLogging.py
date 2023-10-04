import logging as log
import configs as conf
def writeLog(logEntry, logLevel):
 # Configure the logging module
 
 log.basicConfig(filename=conf.log_file, level=log.DEBUG,
                    format='%(asctime)s - %(levelname)s: %(message)s')
 
 if logLevel == "INFO":
       log.info(logEntry)
 elif logLevel == "WARN":
       log.warning(logEntry)
 elif logLevel == "ERROR":
       log.error(logEntry)
