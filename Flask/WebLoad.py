import webLoadFunctions as wb

def loadWebData(url):
# Fetch content from the URL
    source = "WEB"
    curLoadTimeStamp = wb.addLoadHistoryInDB(source)
    dataExists = wb.checkDataExists(url)
    
    if not dataExists:
        web_content = wb.getWebData(url)
        wb.loadDataInDB (source, url, web_content)
    else:
        print(f"Contents of Website: {url} are already present in database.")
        
def loadKBData(url, web_content, web_metadata):
# Fetch content from the URL
    source = "WEB"
    curLoadTimeStamp = wb.addLoadHistoryInDB(source)
    dataExists = wb.checkDataExists(url)
    
    if not dataExists:
        wb.loadKBDataInDB (source, url, web_content, web_metadata)
    else:
        print(f"Contents of Website: {url} are already present in database.")
        
# url = "https://bmcapps.my.site.com/casemgmt/sc_KnowledgeArticle?sfdcid=kA33n000000YIu1CAG"
# loadWebData(url)

    

    

