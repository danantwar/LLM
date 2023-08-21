import psycopg2
# Connect to the PostgreSQL database
conn = psycopg2.connect(host='localhost', database='TestDB', user='postgres', password='Aryan@1986')
# Create a cursor object
cur = conn.cursor()
# Create a table
cur.execute('CREATE TABLE users (id serial PRIMARY KEY, name text, email text)')

# Commit the changes
conn.commit()
# Close the connection
conn.close()
