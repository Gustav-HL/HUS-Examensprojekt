import sqlite3
from pathlib import Path
import json
from array import array
from models.document import Document
from models.chunk import Chunk


# Get the directory where database_test file is located
BASE_DB = Path(__file__).resolve().parent
# Create a path to the database file from repositories folder.
DEFAULT_DB_PATH = BASE_DB / "HUT.db"
# Path to the SQL schema file
DB_SCHEMA_PATH = BASE_DB / "HUT_db.sql"


class LocalDataStorage:
    def __init__(self, DB_PATH=None):
        self.DB_PATH = DB_PATH or DEFAULT_DB_PATH
        self.create_tables()


    def create_tables(self):
        """Create database tables using the SQL schema file."""
        #Read SQL schema file using UTF-8 to support special characters.
        read_sql_file = DB_SCHEMA_PATH.read_text(encoding="utf-8")

        #Connect to the local SQLite database. 
        conn = sqlite3.connect(self.DB_PATH, timeout=30.0)
        try:
            with conn:
                # Enable foreign key checks, to ensure valid relationships between tables.
                conn.execute("PRAGMA foreign_keys = ON")

                #executes the SQL commannds from the schema file.
                conn.executescript(read_sql_file)
        finally:
            conn.close()

    def save_document(self, document):
        """Serialize the document data and runs all data insert at once"""
        document_data = document.serialize_object_data()

        conn = sqlite3.connect(self.DB_PATH, timeout=30.0)
        try:
            with conn:
                conn.execute("PRAGMA foreign_keys = ON")
                self.insert_document_to_db(document, conn=conn, document_data=document_data)
                self.insert_chunks_to_db(document, conn=conn, document_data=document_data)
                self.insert_vectors_to_db(document, conn=conn, document_data=document_data)
        
            print("Data Saved :P")
        
        finally:    
            conn.close()

    def insert_document_to_db(self, document, conn=None, document_data=None):
        """Insert document information into the Documents table."""
        #Get document data as a dictionary. 
        document_data = document_data or document.serialize_object_data()

        keywords = document_data["keywords"]
        metadata = document_data.get("metadata") or {}

        # Convert the data to JSON text. 
        # ensure_ascii=False keeps Swedish characters (å, ä, ö) readable.
        keywords_json = json.dumps(keywords, ensure_ascii=False)


        should_close = conn is None
        conn = conn or sqlite3.connect(self.DB_PATH, timeout=30.0)
        try:
            # Enable foreign key checks, to ensure valid relationships between tables.
            conn.execute("PRAGMA foreign_keys = ON")

            #Insert document inforamation into the Documents table.
            # The (?, ?, ?, ?, ?) are placeholders for the value.
            conn.execute(
                """
                INSERT OR REPLACE INTO Documents (
                    doc_id,
                    title,
                    file_path,
                    file_type,
                    author,
                    creator,
                    creation_date,
                    modification_date,
                    keywords
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    document_data["id"],
                    metadata.get("title") or document_data["name"],
                    document_data["path"],
                    Path(document_data["path"]).suffix,
                    metadata.get("author"),
                    metadata.get("creator"),
                    metadata.get("creation_date"),
                    metadata.get("modification_date"),
                    keywords_json,
                ),
            )
            if should_close:
                conn.commit()
        finally:
            if should_close:
                conn.close()

    def insert_chunks_to_db(self, document, conn=None, document_data=None):
        """Insert document chunk data into the Chunks table."""
        document_data = document_data or document.serialize_object_data()

        # Get the list of chunks from the document.
        chunks = document_data["chunks"]

        should_close = conn is None
        conn = conn or sqlite3.connect(self.DB_PATH, timeout=30.0)
        try:    
            # Enable foreign key, checks to ensure valid relationships between tables.
            conn.execute("PRAGMA foreign_keys = ON")

            # Iterate through each chunk and insert the data into the Chunks table.
            for chunk in chunks:
                entities_json = json.dumps(chunk.get("keynames", []), ensure_ascii=False)
                conn.execute(
                    """
                    INSERT OR REPLACE INTO Chunks (
                        chunk_id,
                        doc_id,
                        chunk_index,
                        entities,
                        text_content
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        chunk["id"],
                        chunk["document_id"],
                        chunk["chunk_index"],
                        entities_json,
                        chunk["text"],
                    ),
                )
            if should_close:
                conn.commit()
        finally:
            if should_close:
                conn.close()

    def insert_vectors_to_db(self, document, conn=None, document_data=None):
        """Insert document chunk vectors into the Vectors table."""
        # Get document data as a dictionary.
        document_data = document_data or document.serialize_object_data()

        # Get the list of chuinks from the document.
        chunks = document_data["chunks"]

        should_close = conn is None
        conn = conn or sqlite3.connect(self.DB_PATH, timeout=30.0)
        try:
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

                # Insert the chunk ID, binary vecyor into the Vector table.
                conn.execute(
                    """
                    INSERT OR REPLACE INTO VECTORS (
                        chunk_id,
                        vector
                    )
                    VALUES (?, ?)
                    """,
                    (
                        chunk_data["id"],
                        vector_binary_data,
                    ),
                )
            if should_close:
                conn.commit()
        finally:
            if should_close:
                conn.close()
                
    def get_document_data(self, conn=None):
        
        should_close = conn is None
        conn = conn or sqlite3.connect(self.DB_PATH, timeout=30.0)
        
        try:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()
            
            query=(
                """
                SELECT * FROM Documents; 
                
                """
                
            )
            cursor.execute(query)
            documents = cursor.fetchall()
            
            for document in documents:
                print(document)

            return documents
            
        
        finally:
                if should_close:
                    conn.close()
                    
                    
                   
        
        #  def serialize_object_data(self) -> dict:
        #          """
        #          Goes through each chunk, checks if there is a valid Vector array appends each chunk to a list.
         
        #              Returns: Dict: containing all data stored in Document
        #          """
        #          gathered_chunks = []
        #          for chunk in self.chunks:
        #              stored_vector = getattr(chunk, "vector", None)
         
        #              if stored_vector is not None and hasattr(stored_vector, "tolist"):
        #                  valid_vector = stored_vector.tolist()
        #              else:
        #                  valid_vector = stored_vector
         
        #              gathered_chunks.append({
        #                  "id": getattr(chunk, "id", None),
        #                  "chunk_index": getattr(chunk, "chunk_index", None),
        #                  "document_id": getattr(chunk, "document_id", self.id),
        #                  "text": getattr(chunk, "text", ""),
        #                  "keywords": getattr(chunk, "keywords", []),
        #                  "keynames": getattr(chunk, "keynames", []),
        #                  "vector": valid_vector,
        #              })
         
        #          return {
        #              "id": self.id,
        #              "name": self.name,
        #              "path": str(self.path),
        #              "raw_text": self.raw_text,
        #              "keywords": self.keywords,
        #              "metadata": self.metadata,
        #              "chunks": gathered_chunks,
        #          } 
                


    
    
    