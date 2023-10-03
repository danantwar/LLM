import SQL_Functions as sq
import datetime

def validateLoad(source):     
    loadHistoryResults = sq.getLastLoadTimestamp(source)     
    lastLoadTimestamp = loadHistoryResults[0]
    loadStatus=loadHistoryResults[1]
    print("Last Load Status: ", loadStatus)
    print("loadHistoryResults:", loadHistoryResults)
   
    if (loadStatus == "Completed" or len(loadStatus) == 0): 
        initiateLoad = True
    else:
        initiateLoad = False
    
    return initiateLoad


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

#-----------------------------------------------------------------

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