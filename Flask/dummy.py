import SQL_Functions as sq

def checkDataExists():
    conn = sq.getconnection()
    source = "HELIX"
    query = "SELECT load_timestamp, load_status FROM public.\"LoadHistory\" WHERE source = '" + source + "' ORDER BY load_timestamp DESC LIMIT 1 "
    dataExists = False
    print(query)
    
    try:
        cursor = conn.cursor()        
        cursor.execute(query)
        records = cursor.fetchall()
        for record in records:
            lastLoadTimestamp = record[0]
            loadStatus=record[1]
            print("loadStatus:", loadStatus)
    except (Exception) as error:
        print("Error while reading records:", error)
    
    conn.close()
    #print(records)

checkDataExists()