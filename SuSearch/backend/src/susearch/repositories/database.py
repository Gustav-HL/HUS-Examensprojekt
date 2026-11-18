import sqlite3
from pathlib import Path
import json
from array import array
from models.document import Document
from models.chunk import Chunk


# Get the directory containing this database file.
BASE_DB = Path(__file__).resolve().parent
# Path to the default database file in the repositories folder.
DEFAULT_DB_PATH = BASE_DB / "HUT.db"
# Path to the SQL schema file
DB_SCHEMA_PATH = BASE_DB / "HUT_db.sql"


class LocalDataStorage:
    """Manages local SQLite storage for documents, chunks and vectors."""
   
    def __init__(self, DB_PATH=None):
        """Set database path and create database tables."""
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
        """Save the document, chunks and vectors in one transaction."""
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
        """Insert document information into the Documents table.
        
        Args:
            document: 
                he Document object that is being saved.
            conn: 
                Existing SQLite connection. If not provided,
                this method opens, commits and closes its own connection.
            document_data: 
                A dictionary that contains serialized document data. 
                If not provided it is created from document.
        """
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
            # The (?, ?, ?, ?, ?) are placeholders for the column value.
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
        """Insert document chunk data into the Chunks table.
        
        Args:
            document: 
                The Document object containing the chunks to save.
            conn: 
                Existing SQLite connection. If not provided,
                this method opens, commits and closes its own connection.
            document_data: 
                A dictionary containing serialized document
                data. If not provided, it is created from document.
        
        """
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
        """Insert document chunk vectors into the Vectors table and skipping empty vector.
        
        Args:
            document: 
                The Document object containing the vectors to save.
            conn: 
                Existing SQLite connection. If not provided,
                this method opens, commits and closes its own connection. 
            document_data: 
                A dictionary containing serialized document
                data. If not provided, it is created from document.       
        """
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
        """Fetch all data from Doucments and structure their metadata as dictionaries. 
        
        Args:
            conn: 
                Existing SQLite connection. If not provided,
                this method opens and closes its own connection.
        
        Returns:
            A list of document dictionaires containing ID, name, path, leywords and metadata.
            Returns an empty list if no documents exsist.
        """    
       
        should_close = conn is None
        conn = conn or sqlite3.connect(self.DB_PATH, timeout=30.0)
        
        try:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()
            cursor.row_factory = sqlite3.Row
            
            query=(
                """
                SELECT * FROM Documents; 
                
                """
                
            )
            cursor.execute(query)
            rows = cursor.fetchall()
            
            documents = []
            
            for document_data in rows:
                document = {
                    "id": document_data["doc_id"],
                    "name": Path(document_data["file_path"]).name,
                    "path": document_data["file_path"],
                    "keywords": json.loads(document_data["keywords"]),
                    "metadata": {
                        "doc_title": document_data["title"],
                        "file_type": document_data["file_type"],
                        "author": document_data["author"],
                        "creator": document_data["creator"],
                        "creation_date": document_data["creation_date"],
                        "modification_date": document_data["modification_date"]
                    }
                }
                
                documents.append(document)
                
            return documents
        
        finally:
                if should_close:
                    conn.close()
                    
                   
                   
    
        
    
    