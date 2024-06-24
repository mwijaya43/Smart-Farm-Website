import sqlite3

# Connect to the SQLite database (replace 'your_database.db' with your actual database file)
conn = sqlite3.connect('C:\Users\pixel\PycharmProjects\pythonProject\Pemograman Berbasis Web\UAS\Smart Farm\SmartFarmProject\db.sqlite3')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Execute a SQL query to fetch data
cursor.execute("SELECT * SmartFarmSystem_SmartPlantingActuator")  # Replace 'your_table_name' with the actual table name

# Fetch all the rows retrieved by the query
rows = cursor.fetchall()

# Process the fetched data (example: print the rows)
for row in rows:
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()
