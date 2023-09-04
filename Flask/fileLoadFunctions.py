import SQL_Functions as sq
import datetime

def addLoadHistoryInDB(source):
    current_datetime = datetime.datetime.now(datetime.timezone.utc)
    load_timestamp = current_datetime.strftime('%m/%d/%Y %H:%M:%S %p')
    
    conn = sq.getconnection() 
    data = (source, load_timestamp)                
    # Insert records in Database table            
    sq.create_loadhistory(conn, data)
    conn.close()

#-----------------------------------------------------------------
def loadDataInDB(source, filename, file_content):
    # Initialize variables
    content_limit = 1000
    content_len = 0
    # Initialize DB Connection
    conn = sq.getconnection()  
    content_len = len(file_content)
    content_splits, content_rem = divmod(content_len, content_limit)
    if content_rem != 0:
        content_splits = content_splits + 1
        for split in range(content_splits):
            content = file_content[split * content_limit : (split + 1) * content_limit]                 
            content_parts = str(split+1) + "/" + str(content_splits)
            content_metadata = content
            data = (source, filename, content, content_metadata, content_parts)                
            # Insert records in Database table            
            sq.create_records(conn, data)    
    print ("Parts: " + str(content_splits))
    # Close DB Connection
    conn.close()
#-----------------------------------------------------------------    