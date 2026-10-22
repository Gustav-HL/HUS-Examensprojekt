import sqlite3

# A in-memory database
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# Create table
cursor.execute("CREATE TABLE dokument (data TEXT);")

# Insert data inro the table
cursor.execute(
    "INSERT INTO dokument (data) VALUES (?)",
    ("Hej | Hejsan | hej",)
)
conn.commit()

# Search
search_term = "%Hej%"
query = "SELECT data FROM dokument WHERE data LIKE ?"

for row in cursor.execute(query, (search_term,)):
    print(f"Match: {row[0]}")

conn.close()