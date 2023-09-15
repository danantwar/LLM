import openAIFunctions as ai
import SQL_Functions as sq
import datetime
import contentSplitter as csplit
import generateEmbeding as ge

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
     # Initialize DB Connection    
    conn = sq.getconnection()
    
    # Code to slpit the contents based on Token limit  
    chunks = ge.generatetokens(file_content)
    for i, chunk in enumerate(chunks):
        content_parts = str(i+1)+ "/" + str(len(chunks))
        content_metadata = chunk.page_content
        content = chunk
        embedding = ge.generateEmbedding(content)
        embedding_list = embedding.tolist()
        data = (source, filename, content, content_metadata, content_parts, embedding_list[0])                
        # Insert records in Database table            
        sq.create_records(conn, data)
    print ("Parts: " + str(len(chunks)))
    
    # # Code to slpit the contents in chunk   
    # chunks = csplit.contentspiltter(file_content)
    # for i, chunk in enumerate(chunks):
    #     content_parts = str(i+1)+ "/" + str(len(chunks))
    #     content_metadata = chunk.page_content
    #     content = chunk.page_content
    #     #embeddings = ai.generateEmbeddings(content, "text-embedding-ada-002")
    #     data = (source, filename, content, content_metadata, content_parts)                
    #     # Insert records in Database table            
    #     sq.create_records(conn, data)
    # print ("Parts: " + str(len(chunks)))

    # Close DB Connection
    conn.close()
#-----------------------------------------------------------------    