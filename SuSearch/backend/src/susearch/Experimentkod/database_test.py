import sqlite3
from pathlib import Path

# Get the directory where database_test file is located
BASE_DB = Path(__file__).resolve().parent

# Create a path to the database file from repositories folder.
DB_PATH = BASE_DB.parent / "repositories" / "HUT_test.db"

def test_database():
    #Connect to sqLite database
    conn = sqlite3.connect(DB_PATH)
    
    # Check that the database file exists
    if not DB_PATH.is_file():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    #Create a cursor to execute SQL queries.
    cursor = conn.cursor()

    # Enable foreign key checks to ensure valid relationships between tables.
    conn.execute("PRAGMA foreign_keys = ON")

    #List of tables to check in database
    tables = ["Documents", "Chunks", "Vectors"]

    # Iterate through each table
    for table in tables:
        print(f"\nTable: {table}")
            
        #Retrive info from the columns in the current table.
        cursor.execute(f"PRAGMA table_info('{table}');")

        # Iterate through the columns and print each column name.
        for column in cursor.fetchall():
            print(column[1])
        
    conn.close()    


if __name__ == "__main__":
    test_database()