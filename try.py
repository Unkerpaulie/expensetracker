import sqlite3

def list_tables_and_columns(db_name):
    # Connect to the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("ALTER TABLE income_incomecategory RENAME TO income_source;")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    # Iterate over all tables
    for table in tables:
        table_name = table[0]
        print(f"Table: {table_name}")
        
        # Get column names for the current table
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        print("Columns:")
        for column in columns:
            print(f" - {column[1]}")
        print()  # Newline for better readability
    
    # Close the connection
    conn.close()

# Call the function with the database name
list_tables_and_columns("db.sqlite3")
