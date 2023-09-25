import psycopg2
from psycopg2 import Error
import DataLoadLogging as logs

# Function to establish a connection to the PostgreSQL database
def getconnection():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="postgres",
            host="localhost",
            port="5435",
            database="postgres"
        )
        return connection
    except (Exception, Error) as error:
        logs.writeLog(f"Error while connecting to PostgreSQL:{error}", "ERROR")
        print("Error while connecting to PostgreSQL:", error)
        return None

#-----------------------------------------------------------------

# Create single record 
def create_records(connection, data):
    try:
        cursor = connection.cursor()
        insert_query = "INSERT INTO public.\"LLM\" (source, reference, content, content_metadata, content_parts, embedding) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, data)
        connection.commit()
       #print("Record inserted successfully")        
    except (Exception, Error) as error:
        logs.writeLog(f"Error while inserting a record::{error}", "ERROR")
        print("Error while inserting a record:", error)

#-----------------------------------------------------------------

# Create bulk records
def createBulkRecords(connection, dataRecords):
    try:
        cursor = connection.cursor()
        insert_query = "INSERT INTO public.\"LLM\" (source, reference, content, content_metadata, content_parts, embedding) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.executemany(insert_query, dataRecords)
        connection.commit()
        logs.writeLog("Records inserted in database successfully.", "INFO")
       #print("Record inserted successfully")        
    except (Exception, Error) as error:
        logs.writeLog(f"Error while inserting a record::{error}", "ERROR")
        print("Error while inserting a record:", error)

#-----------------------------------------------------------------
        
# Create new record in LoadHistory Table
def create_loadhistory(connection, data):
    try:
        cursor = connection.cursor()
        insert_query = "INSERT INTO public.\"LoadHistory\" (source, load_timestamp, load_status) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, data)
        connection.commit()
        logs.writeLog("Data Load History Record Created Successfully.", "INFO")
        print("Load History Record Created Successfully.")        
    except (Exception, Error) as error:
        logs.writeLog(f"Error while inserting a record::{error}", "ERROR")
        print("Error while inserting a record:", error)

#-----------------------------------------------------------------

# Update record in LoadHistory Table
def update_loadHistory(connection, data):
    try:
        cursor = connection.cursor()
        update_query = "update public.\"LoadHistory\" SET load_status = %s WHERE source = %s and load_timestamp = %s"    
        cursor.execute(update_query, data)
        connection.commit()
        logs.writeLog("Data Load History Record Updated Successfully.", "INFO")
        print("Load History Record Updated Successfully")        
    except (Exception, Error) as error:
        logs.writeLog(f"Error while inserting a record:, {error}", "ERROR")
        print("Error while inserting a record:", error)

#-----------------------------------------------------------------

def getLastLoadTimestamp(source):
    conn = getconnection()
    query = "SELECT load_timestamp, load_status FROM public.\"LoadHistory\" WHERE source = '" + source + "' ORDER BY load_timestamp DESC LIMIT 1 "
    lastLoadTimestamp = ""
    loadStatus = ""

    try:
        cursor = conn.cursor()        
        cursor.execute(query)
        records = cursor.fetchall()
        for record in records:
            lastLoadTimestamp = record[0]
            loadStatus=record[1]
            #print("Load History Record: ", record)
    except (Exception) as error:
        logs.writeLog(f"Error while reading records: {error}", "ERROR")
        print("Error while reading records:", error)
    
    conn.close()
    return lastLoadTimestamp, loadStatus

#-----------------------------------------------------------------

# Read operation
def read_records(connection, query):
    try:
        cursor = connection.cursor()
        select_query = query
        cursor.execute(select_query)
        records = cursor.fetchall()
        for record in records:
            print(record)
    except (Exception, Error) as error:
        logs.writeLog(f"Error while reading records: {error}", "ERROR")
        print("Error while reading records:", error)

# Update operation
def update_record(connection, new_data):
    try:
        cursor = connection.cursor()
        update_query = "UPDATE your_table SET name = %s, email = %s WHERE id = %s"
        cursor.execute(update_query, (new_data))
        connection.commit()
        logs.writeLog(f"Database Record updated successfully.", "INFO")        
        #print("Database Record updated successfully.")
    except (Exception, Error) as error:
        logs.writeLog(f"Error while Updating records: {error}", "ERROR")
        print("Error while updating a record:", error)

# Delete operation
def delete_record(connection, id):
    try:
        cursor = connection.cursor()
        delete_query = "DELETE FROM users WHERE id = %s"
        cursor.execute(delete_query, (id))
        connection.commit()
        logs.writeLog(f"Record deleted successfully", "INFO")
        #print("Record deleted successfully.")
    except (Exception, Error) as error:
        print("Error while deleting a record:", error)

con = getconnection()
if con != 0:
 logs.writeLog(f"Failed to conned to Database.", "ERROR")
 #print("DB Connection is Established")

#-----------------------------------------------------------------