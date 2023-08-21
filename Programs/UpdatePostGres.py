import SQL_Functions
# Connect to the PostgreSQL database
#conn = psycopg2.connect(host='localhost', database='TestDB', user='postgres', password='Aryan@1986')
# Create a cursor object
conn = SQL_Functions.create_connection()
cur = conn.cursor()
# Update the name of the user with id 1 to 'John Doe'
cur.execute('UPDATE users SET email = \'aryan@abc.com\' WHERE id = 1')
# Commit the changes
conn.commit()
# Close the connection
conn.close()
