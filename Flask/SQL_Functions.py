import psycopg2
from psycopg2 import Error
import DataLoadLogging as logs
import configs as conf

# Function to establish a connection to the PostgreSQL database
def getconnection():
# Get values from configs
    user = conf.dbuser
    password = conf.dbpassword
    dbhost = conf.host
    dbport = conf.port
    dbname = conf.database
    try:
        connection = psycopg2.connect(user=user,  password=password,  host=dbhost,  port=dbport,  database=dbname ))
        return connection
    except (Exception, Error) as error:
        logs.writeLog(f"Error while connecting to PostgreSQL:{error}", "ERROR")
        return None

#-----------------------------------------------------------------
# Function to Create single record in database table
def create_records(connection, data):
    try:
        cursor = connection.cursor()
        insert_query = "INSERT INTO public.\"LLM\" (source, reference, content, content_metadata, content_parts, embedding) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, data)
        connection.commit()
    except (Exception, Error) as error:
        logs.writeLog(f"Error while inserting a record::{error}", "ERROR")
#-----------------------------------------------------------------
# Function to  Create bulk records in database table
def createBulkRecords(connection, dataRecords):
    try:
        cursor = connection.cursor()
        insert_query = "INSERT INTO public.\"LLM\" (source, reference, content, content_metadata, content_parts, embedding) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.executemany(insert_query, dataRecords)
        connection.commit()
        logs.writeLog("Records inserted in database successfully.", "INFO")
    except (Exception, Error) as error:
        logs.writeLog(f"Error while inserting a record::{error}", "ERROR")

#-----------------------------------------------------------------
# Funtciton to Create new record in LoadHistory Table
def create_loadhistory(connection, data):
    try:
        cursor = connection.cursor()
        insert_query = "INSERT INTO public.\"LoadHistory\" (source, load_timestamp, load_status) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, data)
        connection.commit()
        logs.writeLog("Data Load History Record Created Successfully.", "INFO")
    except (Exception, Error) as error:
        logs.writeLog(f"Error while inserting a record::{error}", "ERROR")
#-----------------------------------------------------------------
# Function to Update record in LoadHistory Table
def update_loadHistory(connection, data):
    try:
        cursor = connection.cursor()
        update_query = "update public.\"LoadHistory\" SET load_status = %s WHERE source = %s and load_timestamp = %s"    
        cursor.execute(update_query, data)
        connection.commit()
        logs.writeLog("Data Load History Record Updated Successfully.", "INFO")
    except (Exception, Error) as error:
        logs.writeLog(f"Error while inserting a record:, {error}", "ERROR")
#-----------------------------------------------------------------
# Function to get last load details for a particular source from LoadHistory Table
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
            print("Load History Record: ", record)
        if len(records) == 0:
            logs.writeLog("There are no records present in database for this query.", "INFO")
        else:
            logs.writeLog(f"There are {len(records)} records found in database for this query.", "INFO")
    except (Exception) as error:
        logs.writeLog(f"Error while reading records: {error}", "ERROR")
    
    conn.close()
    return lastLoadTimestamp, loadStatus
#-----------------------------------------------------------------
# Function to retrieve record from database Table
def read_records(connection, query):
    try:
        cursor = connection.cursor()
        select_query = query
        cursor.execute(select_query)
        records = cursor.fetchall()
    except (Exception, Error) as error:
        logs.writeLog(f"Error while reading records: {error}", "ERROR")
    return records
#-----------------------------------------------------------------
# Function to update record in database Table
def update_record(connection, new_data):
    try:
        cursor = connection.cursor()
        update_query = "UPDATE your_table SET name = %s, email = %s WHERE id = %s"
        cursor.execute(update_query, (new_data))
        connection.commit()
        logs.writeLog(f"Database Record updated successfully.", "INFO")        
    except (Exception, Error) as error:
        logs.writeLog(f"Error while Updating records: {error}", "ERROR")
#-----------------------------------------------------------------
# Function to delete record from database Table
def delete_record(connection, id):
    try:
        cursor = connection.cursor()
        delete_query = "DELETE FROM users WHERE id = %s"
        cursor.execute(delete_query, (id))
        connection.commit()
        logs.writeLog(f"Record deleted successfully", "INFO")
    except (Exception, Error) as error:
        logs.writeLog(f"Error while deleting a record:{error}", "ERROR")
#-----------------------------------------------------------------