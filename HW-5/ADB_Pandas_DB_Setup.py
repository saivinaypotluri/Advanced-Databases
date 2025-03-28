import mysql.connector
import pandas as pd

# Set up MySQL connection (use your own credentials)
db_connection = mysql.connector.connect(
    host="localhost",  # Or your MySQL server IP if remote
    user="ADB",  # Your MySQL username
    password="Saivinay@333",  # Your MySQL password
    database="Customer_shopping"  # Database you want to work with
)

# Create a cursor object to execute SQL queries
cursor = db_connection.cursor()

# Query to fetch all table names from the database
cursor.execute("SHOW TABLES")

# Get all table names
tables = cursor.fetchall()

# Dictionary to hold table field names
tables_and_fields = {}

# Fetching column names (fields) for each table
for table in tables:
    table_name = table[0]
    cursor.execute(f"DESCRIBE {table_name}")
    fields = cursor.fetchall()
    # Extract column names for each table
    field_names = [field[0] for field in fields]
    tables_and_fields[table_name] = field_names

# Print the tables and their fields
print("SQL Tables and Fields:")
for table, fields in tables_and_fields.items():
    print(f"\nTable: {table}")
    print("Fields:", ", ".join(fields))

# Fetching sample data (first 5 rows) from each table
print("\nSample Data (First 5 rows) from Each Table:")
for table in tables_and_fields:
    cursor.execute(f"SELECT * FROM {table} LIMIT 5")  # Adjust LIMIT for sample size
    sample_data = cursor.fetchall()
    # Display the sample data using pandas for nice formatting
    df = pd.DataFrame(sample_data, columns=tables_and_fields[table])
    print(f"\nTable: {table}")
    print(df)

# Close the cursor and database connection
cursor.close()
db_connection.close()
