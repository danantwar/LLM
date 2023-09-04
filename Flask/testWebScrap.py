from selenium import webdriver
from bs4 import BeautifulSoup


# URL of the website you want to scrape
#url = 'https://docs.bmc.com/docs/smartit2105/learning-about-problem-management-1002909081.html'
url= 'https://bmcapps.my.site.com/casemgmt/sc_KnowledgeArticle?sfdcid=kA33n000000TWH8CAO&type=ProductDescription'

# Set up a Selenium WebDriver (you need to have the appropriate driver installed)
# For example, if using Chrome, download the ChromeDriver and provide its path
#chromedriverpath = r'C:\Users\jagadish.patil\myTestEnv\LLM Project\LLM\chromedriver-win64\chromedriver.exe'
#print(chromedriverpath)
#driver = webdriver.Chrome(chromedriverpath)
driver = webdriver.Chrome()
#driver.get(url)

# Load the page using the WebDriver
driver.get(url)

# Get the page source after waiting for a bit to allow JavaScript content to load
driver.implicitly_wait(10)  # Wait for 10 seconds
page_source = driver.page_source

# Close the WebDriver


# Parse the HTML content of the page using BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Find the main content element based on its class
main_content = soup.find('div', class_='support-search-areas')


# Extract and print the text content from the main content element
if main_content:
    content_text = main_content.get_text()
    print(content_text)
else:
    print("Main content not found.")
