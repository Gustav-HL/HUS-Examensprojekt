from pathlib import Path  
from susearch.repositories.database import LocalDataStorage
from susearch.models.document import Document
from susearch.models.chunk import Chunk

# Get the path to the repositories folder.
REPOSITORIES_PATH = Path(__file__).resolve().parent.parent / "src" / "susearch" / "repositories"

# Set the path for the test database.
TEST_DB_PATH = REPOSITORIES_PATH / "HUT_test.db"

# Create a storage instance using the test database.
test_storage = LocalDataStorage(DB_PATH=TEST_DB_PATH)

# Create the database tables.
test_storage.create_tables()    
    
    
    
# Create a test document.
test_document = Document(
    name="Test_document.pdf",
    path=Path("Test_document.pdf"),
    raw_text="Detta är ett testdokument för att lagra vectorer och annat trevligt."
    )
    
    
    
# Create a test chunk with a vector.
test_chunk = Chunk(
    text="Detta är ett testdokument för att lagra vectorer och annat trevligt.",
    source="Test_document.pdf",
    keywords=[],
    keynames=[],
    vector=[0.1, 0.2, 0.3]
)

# Add the chunk to the test document.
test_document.add_chunk(test_chunk)    
    
    
# Insert the test document into the database.
test_storage.insert_document_to_db(test_document)

# Insert the test chunk into the database.
test_storage.insert_chunks_to_db(test_document)

# Insert the test vector into the database.
test_storage.insert_vectors_to_db(test_document)
    
    
    
 
    
    
 # def test_database(self, document):
#     """
        
#         Args: document(Document): Object representing a Document storing all data extracted from one document
#     """
# Connect to sqLite database
    # conn = sqlite3.connect(self.DB_PATH)

    # Check that the database file exists
    # if not self.DB_PATH.is_file():
    #     raise FileNotFoundError(f"Database not found: {self.DB_PATH}")
        
    # print(document)

    # #Create a cursor to execute SQL queries.
    # cursor = conn.cursor()

    # # Enable foreign key checks to ensure valid relationships between tables.
    # conn.execute("PRAGMA foreign_keys = ON")

    # #List of tables to check in database
    # tables = ["Documents", "Chunks", "Vectors"]

    # # Iterate through each table
    # for table in tables:
    #     print(f"\nTable: {table}")
                
    #     #Retrive info from the columns in the current table.
    #     cursor.execute(f"PRAGMA table_info('{table}');")

    #     # Iterate through the columns and print each column name.
    #     for column in cursor.fetchall():
    #         print(column[1])
        
    # conn.close()    



def print_data(self):
     pass