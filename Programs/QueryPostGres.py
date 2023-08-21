import SQL_Functions
# Connect to the PostgreSQL database
conn = SQL_Functions.create_connection()
# Create a cursor object
cur = conn.cursor()
# Select all rows from the users table
cur.execute('SELECT * FROM users')
# Fetch all rows
rows = cur.fetchall()

# Print all rows
for row in rows:
    id = row[0]
    Name = row[1]
    Email = row[2]
    print(id, Name)
# Close the connection
conn.close()
