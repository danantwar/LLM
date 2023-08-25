import requests
from SQL_Functions import create_connection as dbconnection
from SQL_Functions import create_datarecords as loadrecord


def loadWebData (url):

    content_limit =1000

    # Fetch content from the URL
    response = requests.get(url)
    web_data = response.text

    # Create a Postgres database connection
    conn = dbconnection()

    content_len = len(web_data)
    content_splits, content_rem = divmod(content_len, content_limit)
    if content_rem != 0:
        content_splits = content_splits + 1
    
    for split in range(content_splits):
        content = web_data[split * content_limit : (split + 1) * content_limit]                 
        content_parts = str(split+1) + "/" + str(content_splits)

    data = ('WEB', url, content, content_parts)

    # Insert the fetched content into the table
    loadrecord(conn, data)

    # Close the connection
    conn.close()
