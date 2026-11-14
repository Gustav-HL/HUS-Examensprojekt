import sqlite3
from pathlib import Path

from susearch.repositories.database import LocalDataStorage
from susearch.models.document import Document
from susearch.models.chunk import Chunk


def test_insert_document_chunks_and_vectors(tmp_path):
    """Check that a document, its chunk and vector are saved."""

    # Use a new temporary database for each test run.
    test_db_path = tmp_path / "HUT_test.db"

    test_storage = LocalDataStorage(DB_PATH=test_db_path)
    test_storage.create_tables()

    # Create a test document.
    test_document = Document(
        name="Test_document.pdf",
        path=Path("Test_document.pdf"),
        raw_text="Detta är ett testdokument."
    )

    # Create a test chunk with a vector.
    test_chunk = Chunk(
        text="Detta är ett testdokument.",
        source="Test_document.pdf",
        keywords=[],
        keynames=[],
        vector=[0.1, 0.2, 0.3]
    )

    test_document.add_chunk(test_chunk)

    # Insert the document, chunk and vector.
    test_storage.insert_document_to_db(test_document)
    test_storage.insert_chunks_to_db(test_document)
    test_storage.insert_vectors_to_db(test_document)

    # Check that each table contains one row.
    with sqlite3.connect(test_db_path) as conn:
        assert conn.execute(
            "SELECT COUNT(*) FROM Documents"
        ).fetchone()[0] == 1

        assert conn.execute(
            "SELECT COUNT(*) FROM Chunks"
        ).fetchone()[0] == 1

        assert conn.execute(
            "SELECT COUNT(*) FROM Vectors"
        ).fetchone()[0] == 1
    
    
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