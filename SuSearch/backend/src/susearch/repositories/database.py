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
        file_path = Path(document_data["path"])

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
                    file_path.name,
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

    def get_document_data_with_chunk_id(self, chunk_ids: list[str], conn=None) -> list[dict]:
        """Fetch document data that the list of chunks belong to.
        
        Args:
            chunk_ids:
                A list of chunk_ids.

            conn: 
                Existing SQLite connection. If not provided,
                this method opens and closes its own connection.

        Returns:
            A list of dictionaries holding the document data.
        """
        
        if not chunk_ids:
            return []
        
        should_close = conn is None
        conn = conn or sqlite3.connect(self.DB_PATH, timeout=30.0)

        try:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()
            cursor.row_factory = sqlite3.Row

            placeholders = ",".join("?" * len(chunk_ids))
            
            query = f"""
                SELECT DISTINCT d.*
                FROM Documents d
                JOIN Chunks c ON c.doc_id = d.doc_id
                WHERE c.chunk_id IN ({placeholders})
            """
            cursor.execute(query, chunk_ids)
            rows = cursor.fetchall()
            
            documents = []
            for document_data in rows:
                documents.append({
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
                        "modification_date": document_data["modification_date"],
                    },
                })
                
            return documents
        
        finally:
                if should_close:
                    conn.close()


    def get_all_chunk_vectors(self, conn=None) -> dict[str, list[float]]:
        """Fetch the vectors of all chunks.

        Args:
            conn:
                Existing SQLite connection. If not provided,
                this method opens and closes its own connection.

        Returns:
            A dictionary that maps chunk_id to its vector (a list of floats).
            Returns an empty dictionary if no vectors exist.
        """
        should_close = conn is None
        conn = conn or sqlite3.connect(self.DB_PATH, timeout=30.0)

        try:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()
            cursor.row_factory = sqlite3.Row

            cursor.execute("SELECT chunk_id, vector FROM Vectors")
            rows = cursor.fetchall()

            vectors = {}
            for row in rows:
                # Convert the binary data back into a float 32-bit array.
                vector_float_array = array("f")
                vector_float_array.frombytes(row["vector"])

                vectors[row["chunk_id"]] = vector_float_array.tolist()

            return vectors

        finally:
            if should_close:
                conn.close()

    def get_document_names_for_chunks(self, chunk_ids: list[str], conn=None) -> dict[str, str]:
        if not chunk_ids:
            return {}

        should_close = conn is None
        conn = conn or sqlite3.connect(self.DB_PATH, timeout=30.0)
        try:
            placeholders = ",".join("?" * len(chunk_ids))
            rows = conn.execute(
                f"""
                SELECT c.chunk_id, d.file_path
                FROM Chunks c
                JOIN Documents d ON d.doc_id = c.doc_id
                WHERE c.chunk_id IN ({placeholders})
                """,
                chunk_ids,
            ).fetchall()
            return {chunk_id: Path(file_path).name for chunk_id, file_path in rows}
        finally:
            if should_close:
                conn.close()


    def get_documents_with_keywords(self, conn=None):
        """
        Function to get the table data and format the keywords for keyword matching
        
        """
        rows = self.get_document_data(conn=conn)

        documents = []
        for row in rows:
            keywords = row[-1]  # Final column in table
            documents.append({
                "doc_id": row[0],
                "title": row[1],
                "file_path": row[2],
                "keywords": json.loads(keywords) if keywords else [],
            })

        return documents

    def get_all_document_ner(self, conn=None) -> dict[str, list]:
        """
        Fetches all NER entities for documents
        
        """
        should_close = conn is None
        conn = conn or sqlite3.connect(self.DB_PATH, timeout=30.0)

        try:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()
            cursor.execute("SELECT doc_id, entities FROM Chunks;")

            ner_by_doc = {}
            for doc_id, raw_ner in cursor.fetchall():
                parsed = (
                    json.loads(raw_ner)
                    if isinstance(raw_ner, str) and raw_ner.strip().startswith("[")
                    else []
                )
                ner_by_doc.setdefault(doc_id, []).append(parsed)

            return ner_by_doc

        finally:
            if should_close:
                conn.close()

    def get_all_chunks(self, conn=None) -> list[Chunk]:
        should_close = conn is None
        conn = conn or sqlite3.connect(self.DB_PATH, timeout=30.0)

        try: 
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()
            cursor.row_factory = sqlite3.Row

            cursor.execute(
                """
                SELECT c.chunk_id, c.doc_id, c.entities, c.text_content,
                    d.file_path, v.vector
                FROM Chunks c
                JOIN Documents d ON d.doc_id = c.doc_id
                LEFT JOIN Vectors v ON v.chunk_id = c.chunk_id
                ORDER BY c.doc_id, c.chunk_index
                """
            )

            rows = cursor.fetchall()

            chunks = []
            for row in rows:
                raw_entities = row["entities"]
                keynames = json.loads(raw_entities) if raw_entities else []
                vector = []
                if row["vector"] is not None:
                    vector_float_array = array("f")
                    vector_float_array.frombytes(row["vector"])
                    vector = vector_float_array.tolist()

                chunks.append(
                    Chunk(
                        text=row["text_content"],
                        source=row["file_path"],
                        keywords=[],
                        keynames=keynames,
                        vector=vector,
                        id=row["chunk_id"],
                        doc_id=row["doc_id"]
                    )
                )

            return chunks
    def get_first_chunk_texts(self, doc_ids: list[str], conn=None) -> dict[str, str]:
        """
        Fetch text of the first chunk to present the first text part as preview in frontend
        
        """
        if not doc_ids:
            return {}

        should_close = conn is None
        
        conn = conn or sqlite3.connect(self.DB_PATH, timeout=30.0)
        try:

            placeholders = ",".join("?" * len(doc_ids))
            rows = conn.execute(
                f"""
                SELECT doc_id, text_content
                FROM Chunks
                WHERE doc_id IN ({placeholders})
                  AND chunk_index = 1
                """,
                doc_ids,
            ).fetchall()

            return {doc_id: text_content for doc_id, text_content in rows}
        
        finally:
            if should_close:
                conn.close()