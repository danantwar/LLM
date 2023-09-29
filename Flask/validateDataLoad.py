import SQL_Functions as sq

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
