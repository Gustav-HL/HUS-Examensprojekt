import sqlite3
from pathlib import Path

# Get the directory where database_test file is located
BASE_DB = Path(__file__).resolve().parent

# Create a path to the database file from repositories folder.
DB_PATH_TEST = BASE_DB / "HUT_test.db"

class LocalDataStorage:
    def __init__(self, DB_PATH):
        self.DB_PATH = DB_PATH
    
    def test_database(self, document):
        #Connect to sqLite database
        conn = sqlite3.connect(self.DB_PATH)
        print(document)
        # Check that the database file exists
        if not self.DB_PATH.is_file():
            raise FileNotFoundError(f"Database not found: {self.DB_PATH}")

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


    def print_data():
        pass

if __name__ == "__main__":

    # 1. Instansiera klassen med DB_PATH
  storage = LocalDataStorage(DB_PATH_TEST)

  # 2. Anropa metoden på objektet (Python skickar med 'self' automatiskt)
  storage.test_database(document=None)