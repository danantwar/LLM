from bs4 import BeautifulSoup
import requests
import re
import webLoad as web

def extractWebPage(url, page_source):
# Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

# Find all the div elements with class "action-detail"
    action_details = soup.find_all("div", class_="action-detail")

# Initialize a dictionary to store labels and values
    label_value_dict = {}

# Iterate through each "action-detail" div
    for action_detail in action_details:
        # Find the label text within the "action-label" div
        label = action_detail.find("div", class_="action-label").text.strip()

        # Find the value within the "action-value" div
        value = action_detail.find("div", class_="action-value").text.strip()

        # Add the label and value to the dictionary
        label_value_dict[label] = value

# extracte labels and values and load into DB
    content=""
    contentMetaData=""
    for label, value in label_value_dict.items():
        #print(f"{label}: {value}")
        contentMetaData = contentMetaData + (f"{label}: {value}" +"\n")
        content= content +" "+ value
    web.loadKBData(url, content, contentMetaData)
  
# Define a regular expression pattern to match URLs
url_pattern = r'https?://\S+'

# Open the file for reading
myFile = 'C:\\Users\\jagadish.patil\\myTestEnv\\Files\\BMCKBList1.txt'
with open(myFile, 'r') as file:
    # Loop through each line in the file
    for line in file:
        # Use re.findall to find all URLs in the current line
        urls = re.findall(url_pattern, line)
        
        for url in urls:
            print(url)
            
            # Fetch the content of the URL using requests
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    page_content = response.text
                    extractWebPage(url, page_content)                    
                else:
                    print(f"Failed to fetch URL: {url}, Status code: {response.status_code}")
            except Exception as e:
                print(f"Error fetching URL: {url}, Error: {e}")