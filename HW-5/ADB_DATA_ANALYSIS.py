import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set up the connection to MySQL (replace with your own credentials)
db_connection = mysql.connector.connect(
    host="localhost",  
    user="ADB",  
    password="Saivinay@333", 
    database="Customer_shopping"
)

# Create a cursor object to interact with the database
cursor = db_connection.cursor()

# Step 1: List all tables in the database
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

# Step 2: Dictionary to store table names and fields
tables_and_fields = {}

# Fetch the fields (columns) of each table
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

# Step 3: Fetching sample data (first 5 rows) from each table and loading into pandas DataFrame
print("\nSample Data (First 5 rows) from Each Table:")
for table in tables_and_fields:
    cursor.execute(f"SELECT * FROM {table} LIMIT 5")  # Adjust LIMIT for sample size
    sample_data = cursor.fetchall()
    # Display the sample data using pandas for nice formatting
    df = pd.DataFrame(sample_data, columns=tables_and_fields[table])
    print(f"\nTable: {table}")
    print(df)

    # Basic data analysis on the DataFrame
    print("\nBasic Info:")
    print(df.info())

    print("\nSummary Statistics:")
    print(df.describe())

    print("\nMissing Values:")
    print(df.isnull().sum())

    # Plotting: For numerical columns, plot the distribution
    if df.select_dtypes(include=['float64', 'int64']).shape[1] > 0:
        plt.figure(figsize=(10, 6))
        sns.histplot(df.select_dtypes(include=['float64', 'int64']).iloc[:, 0], kde=True)
        plt.title(f'Distribution of {table} Data')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.show()

# Step 4: Example - Count of records in each table (optional)
print("\nCount of records in each table:")
for table in tables_and_fields:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"{table}: {count} rows")

# Step 5: Example - Calculate average salary by department (if applicable)
if "employees" in tables_and_fields and "salary" in tables_and_fields["employees"]:
    df_employees = pd.read_sql("SELECT * FROM employees", db_connection)
    avg_salary_by_dept = df_employees.groupby('department')['salary'].mean()
    print("\nAverage Salary by Department:")
    print(avg_salary_by_dept)

# Close the cursor and database connection
cursor.close()
db_connection.close()
