import os
import sqlite3

# Define paths
DATA_FOLDER = "src/data"
SQL_SCRIPT = "db_init.sql"

# Ensure "data" folder exists
os.makedirs(DATA_FOLDER, exist_ok=True)

# Connect to SQLite (change this for other DBs)
db_path = os.path.join(DATA_FOLDER, "database.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if SQL script exists
if not os.path.exists(SQL_SCRIPT):
    print(f"Error: {SQL_SCRIPT} not found!")
else:
    # Run SQL script
    with open(SQL_SCRIPT, "r") as file:
        sql_script = file.read()
    
    try:
        cursor.executescript(sql_script)
        conn.commit()
        print(f"Executed {SQL_SCRIPT} successfully!")
    except sqlite3.Error as e:
        print(f"SQL execution error: {e}")

# Close connection
cursor.close()
conn.close()