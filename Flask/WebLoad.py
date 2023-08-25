import requests
from SQL_Functions import create_connection as dbconnection
from SQL_Functions import create_datarecords as loadrecord
from bs4 import BeautifulSoup

#def loadWebData (url):
url = "https://support.microsoft.com/en-us/topic/kb5014754-certificate-based-authentication-changes-on-windows-domain-controllers-ad2c23b0-15d8-4340-a468-4d4f3b188f16"
content_limit =1000

# Fetch content from the URL

response = requests.get(url)
web_data = response.text

soup = BeautifulSoup(web_data, 'html.parser')

if soup.body:
    # Example: Extract all paragraph text within the body
    web_data = soup.body.find_all('p')

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

print(data)

# Insert the fetched content into the table
loadrecord(conn, data)

# Close the connection
conn.close()
