import SQL_Functions as sq

def checkDataExists(url):
    conn = sq.getconnection()
    query = "SELECT content FROM public.\"LLMData\" WHERE reference = '" + url + "'"
    dataExists = False
    
    print(query)
    
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


url = "https://support.microsoft.com/en-us/topic/kb5014754-certificate-based-authent"
exist = checkDataExists(url)
print(exist)
