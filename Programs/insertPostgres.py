import SQL_Functions

# Connect to the PostgreSQL database
conn = SQL_Functions.create_connection()

# Create a cursor object
cur = conn.cursor()

# Create a record to insert
record = ('Ajit Patil', 'ajit@gmail.com')

# Insert the record into the table
cur.execute('INSERT INTO users (name, email) VALUES (%s, %s)', record)

# Commit the changes
conn.commit()

# Close the connection
conn.close()