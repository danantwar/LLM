import re
from bs4 import BeautifulSoup
import requests
import openAIFunctions as ai
import datetime
import SQL_Functions as sq


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
    # Initialize variables
    #content_limit = 1000
    #content_len = 0
    content_metadata = web_content
    # using web scrapping need ot extract key value pair data form web page and store it in content variable
    content = web_content
    
    '''
    content_len = len(web_content)
    content_splits, content_rem = divmod(content_len, content_limit)
    if content_rem != 0:
        content_splits = content_splits + 1
        for split in range(content_splits):
            content = web_content[split * content_limit : (split + 1) * content_limit]                 
            content_parts = str(split+1) + "/" + str(content_splits)
    '''
    
    # Initialize DB Connection
    conn = sq.getconnection()  
    content_parts = "1/1"
    embeddings = ai.generateEmbeddings(content, "text-embedding-ada-002")
    data = (source, url, content, content_metadata, content_parts)
    # Insert records in Database table            
    sq.create_records(conn, data)    
    #print ("Parts: " + str(content_splits))
    # Close DB Connection
    conn.close()
#-----------------------------------------------------------------    
#-----------------------------------------------------------------
def loadKBDataInDB(source, url, web_content, web_metadata):
    # Initialize variables
    #content_limit = 1000
    #content_len = 0
    content_metadata = web_metadata
    # using web scrapping need ot extract key value pair data form web page and store it in content variable
    content = web_content
    embeddings = ai.generateEmbeddings(content, "text-embedding-ada-002")
    '''
    content_len = len(web_content)
    content_splits, content_rem = divmod(content_len, content_limit)
    if content_rem != 0:
        content_splits = content_splits + 1
        for split in range(content_splits):
            content = web_content[split * content_limit : (split + 1) * content_limit]                 
            content_parts = str(split+1) + "/" + str(content_splits)
    '''
    
    # Initialize DB Connection
    conn = sq.getconnection()  
    content_parts = "1/1"
    data = (source, url, content, content_metadata, content_parts)
    # Insert records in Database table            
    sq.create_records(conn, data)    
    #print ("Parts: " + str(content_splits))
    # Close DB Connection
    conn.close()
#-----------------------------------------------------------------    