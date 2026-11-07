import sqlite3

#Connect to sqLite database
conn = sqlite3.connect("/Users/marina/Documents/Informationsarkitekt_HT26_VT_27/DA485A-Examensprojekt/HUT_test.db")

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