import re
from bs4 import BeautifulSoup
import requests
import openAIFunctions as ai
import datetime
import SQL_Functions as sq
import contentSplitter as csplit
import generateEmbeding as ge


#-----------------------------------------------------------------
def addLoadHistoryInDB(source):
    current_datetime = datetime.datetime.now(datetime.timezone.utc)
    load_timestamp = current_datetime.strftime('%m/%d/%Y %H:%M:%S %p')
    
    conn = sq.getconnection() 
    data = (source, load_timestamp)                
    # Insert records in Database table            
    sq.create_loadhistory(conn, data)
    conn.close()
    return load_timestamp
#-----------------------------------------------------------------
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
def remove_extra_line_breaks(text):
    # Remove extra line breaks and whitespace
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
#-----------------------------------------------------------------
def getWebData (url):
    response = requests.get(url)
    if response.status_code == 200:
        page_content = response.text
    else:
        print(f"Failed to fetch webpage content. Status code: {response.status_code}")
        exit()

    soup = BeautifulSoup(page_content, 'html.parser')
    text_content = soup.get_text()
    web_content = remove_extra_line_breaks(text_content)
    
    return web_content
#-----------------------------------------------------------------
def loadDataInDB(source, url, web_content):

    content_metadata = web_content
    content = web_content
    
    # Initialize DB Connection
    conn = sq.getconnection() 
    
    # Code to slpit the contents based on Token limit   
    chunks = ge.generatetokens(content)
    for i, chunk in enumerate(chunks):
        content_parts = str(i+1)+ "/" + str(len(chunks))
        content_metadata = content_metadata
        content = chunk
        embedding = ge.generateEmbedding(content)
        embedding_list = embedding.tolist()
        data = (source, url, content, content_metadata, content_parts, embedding_list[0])             
        # Insert records in Database table            
        sq.create_records(conn, data) 
    
    # # Code to slpit the contents in chunk  
    # chunks = csplit.contentspiltter(content)
    # for i, chunk in enumerate(chunks):
    #     content_parts = str(i+1)+ "/" + str(len(chunks))
    #     content_metadata = content_metadata
    #     content = chunk.page_content
    #     #embeddings = ai.generateEmbeddings(content, "text-embedding-ada-002")
    #     #print(embeddings)
    #     data = (source, url, content, content_metadata, content_parts)             
    #     # Insert records in Database table            
    #     sq.create_records(conn, data)   

    # Close DB Connection
    conn.close()
#-----------------------------------------------------------------    
#-----------------------------------------------------------------
def loadKBDataInDB(source, url, web_content, web_metadata):

    content_metadata = web_metadata
    content = web_content

    # Initialize DB Connection
    conn = sq.getconnection() 
    # Code to slpit the contents based on Token limit   
    chunks = ge.generatetokens(content)
    for i, chunk in enumerate(chunks):
        content_parts = str(i+1)+ "/" + str(len(chunks))
        content_metadata = content_metadata
        content = chunk
        embedding = ge.generateEmbedding(content)
        embedding_list = embedding.tolist()
        data = (source, url, content, content_metadata, content_parts, embedding_list[0])             
        # Insert records in Database table            
        sq.create_records(conn, data)
        
    # # Code to slpit the contents in chunk  
    # chunks = csplit.contentspiltter(content)
    # for i, chunk in enumerate(chunks):
    #     content_parts = str(i+1)+ "/" + str(len(chunks))
    #     content_metadata = content_metadata
    #     content = chunk.page_content
    #     #embeddings = ai.generateEmbeddings(content, "text-embedding-ada-002")
    #     #print(embeddings)
    #     data = (source, url, content, content_metadata, content_parts)             
    #     # Insert records in Database table            
    #     sq.create_records(conn, data)
    
    # Close DB Connection
    conn.close()
#-----------------------------------------------------------------    