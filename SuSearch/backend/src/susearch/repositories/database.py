import sqlite3
from pathlib import Path
import json
from array import array
from susearch.models.document import Document
from susearch.models.chunk import Chunk


# Get the directory where database_test file is located
BASE_DB = Path(__file__).resolve().parent
# Create a path to the database file from repositories folder.
DEFAULT_DB_PATH = BASE_DB / "HUT.db"
#Path to the SQL schema file
DB_SCHEMA_PATH = BASE_DB /"HUT_db.sql"

class LocalDataStorage:
    def __init__(self, DB_PATH=None):
        self.DB_PATH = DB_PATH or DEFAULT_DB_PATH
        
    def create_tables(self):
        """Create database tables using the SQL schema file.""" 
        
        #Read SQL schema file using UTF-8 to support special characters.
        read_sql_file = DB_SCHEMA_PATH.read_text(encoding="utf-8")   
        
        #Connect to the local SQLite database. 
        with sqlite3.connect(self.DB_PATH) as conn:
            
            # Enable foreign key checks, to ensure valid relationships between tables.
            conn.execute("PRAGMA foreign_keys = ON")
            
            #executes the SQL commannds from the schema file.
            conn.executescript(read_sql_file)
            
    
    def insert_document_to_db(self, document):   
        """Insert document information into the Documents table."""  
        
        #Get document data as a dictionary. 
        document_data = document.serialize_object_data()
        
        #Get keywords and metadata from the document.
        keywords = document_data["keywords"]
        metadata = document_data["metadata"]
        
        
        # Convert the data to JSON text. 
        # ensure_ascii=False keeps Swedish characters (å, ä, ö) readable.
        keywords_json = json.dumps(keywords, ensure_ascii=False)
        metadata_json = json.dumps(metadata, ensure_ascii=False)
        
        with sqlite3.connect(self.DB_PATH) as conn:
            
            #Insert document inforamation into the Documents table.
            # The (?, ?, ?, ?, ?) are placeholders for the value.
            conn.execute("""
                INSERT INTO Documents (
                    doc_id,
                    title,
                    file_path,
                    keywords,
                    metadata
                )
                VALUES (?, ?, ?, ?, ?) 
                """, 
                (
                    document_data["id"],
                    document_data["name"],
                    document_data["path"],
                    keywords_json,
                    metadata_json    
                )
            )
            
    def insert_chunks_to_db(self, document):   
        """ Insert document chunk data into the Chunks table """
            
        document_data = document.serialize_object_data()
            
        # Get the list of chunks from the document.
        chunks = document_data["chunks"] 
        
        with sqlite3.connect(self.DB_PATH) as conn:
            
            # Enable foreign key, checks to ensure valid relationships between tables.
            conn.execute("PRAGMA foreign_keys = ON")

            # Iterate through each chunk and insert the data into the Chunks table.
            for chunk in chunks:
                conn.execute( """ 
                                INSERT INTO Chunks (
                                    chunk_id,
                                    doc_id,
                                    chunk_index,
                                    text_content
                                )
                                VALUES (?, ?, ?, ?)
                              """,
                              (
                                  chunk["id"],
                                  chunk["document_id"],
                                  chunk["chunk_index"],
                                  chunk["text"]
                              )
                            )
    
    def insert_vectors_to_db(self, document):
        """ Insert document chunk vectors into the Vectors table. """   
        
        # Get document data as a dictionary.
        document_data = document.serialize_object_data()
        
        # Get the list of chuinks from the document.
        chunks = document_data["chunks"]
        
        # Connect to local database.
        with sqlite3.connect(self.DB_PATH) as conn:
            
            # Check foregin keys and ensure valid relationships between tables.
            conn.execute("PRAGMA foreign_keys = ON")

            # Iterate through each chunk and get its vector.
            for chunk_data in chunks:
                vector = chunk_data["vector"]
                
                # Skip the chunk if vector is missing or is empty.
                if vector is None or len(vector) == 0:
                    continue
                    
                # convert vector values into a float 32-bit array.
                vector_float_array = array("f", vector)
                    
                # convert the float 32 bit array into binary data.
                vector_binary_data = vector_float_array.tobytes()
                
                # Get the number of dimensions in the vector.
                vector_dimensions = len(vector)
                
                # Insert the chunk ID, binary vecyor and dimensions into the Vector table.    
                conn.execute( """
                                INSERT INTO VECTORS(
                                chunk_id,
                                vector,
                                dimensions
                            )
                                VALUES( ?, ?, ?)  
                            """, 
                                (
                                    chunk_data["id"],
                                    vector_binary_data,
                                    vector_dimensions
                                )     
                            )
                

    



    
    
  