import sqlite3

conn = sqlite3.connect('my_database.sqlite')
cursor = conn.cursor()

# Example query: select all from the 'tilat' table
cursor.execute("SELECT * FROM tilat")
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row)

# Close the connection
conn.close()
