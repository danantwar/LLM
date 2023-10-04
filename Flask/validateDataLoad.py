import SQL_Functions as sq
import datetime

#-----------------------------------------------------------------------------
# This Function will check if the previous data load for particular source is still running or completed
def validateLoad(source):     
    loadHistoryResults = sq.getLastLoadTimestamp(source)     
    lastLoadTimestamp = loadHistoryResults[0]
    loadStatus=loadHistoryResults[1]

    if (loadStatus == "Completed" or len(loadStatus) == 0): 
        initiateLoad = True
    else:
        initiateLoad = False
    
    return initiateLoad
#-----------------------------------------------------------------------------
# This Function will create a new data load record for particular source in LoadHistory table
def createLoadHistoryInDB(source):
    current_datetime = datetime.datetime.now(datetime.timezone.utc)
    loadTimestamp = current_datetime.strftime('%m/%d/%Y %H:%M:%S %p')
    loadStatus = "Running"
    conn = sq.getconnection() 
    data = (source, loadTimestamp, loadStatus)
    # Insert records in Database table
    sq.create_loadhistory(conn, data)
    conn.close()
    return loadTimestamp, loadStatus

#-----------------------------------------------------------------------------
# This Function will update a data load record in LoadHistory table
def updateLoadHistory(args):
    # Extract arguments
    loadStatus = args[0]
    source = args[1]
    loadTimestamp = args[2]
    conn = sq.getconnection() 
    data = (loadStatus, source, loadTimestamp)
    # Insert records in Database table
    sq.update_loadHistory(conn, data)
    conn.close()
#-----------------------------------------------------------------------------