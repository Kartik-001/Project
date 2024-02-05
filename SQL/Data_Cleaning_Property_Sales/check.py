import mysql.connector

# Replace these values with your MySQL server information
host = 'localhost'
user = 'root'
password = 'data'
database = 'nashville_housing'

# Create a MySQL connection with the specified database
connection = mysql.connector.connect(
   host=host,
   user=user,
   password=password,
   database=database
)

table_name = 'propertysales'  # Replace with your table name

try:
   # Create a cursor object to execute SQL commands
   cursor = connection.cursor()

   # Execute a SELECT query on the table
   query = f"SELECT * FROM {table_name}"
   cursor.execute(query)

   # Fetch all rows from the result set
   rows = cursor.fetchall()

   # Display the contents of the table
   print(f"Contents of table {table_name}:")
   for row in rows:
       print(row)

finally:
   # Close the cursor and the connection
   cursor.close()
   connection.close()
