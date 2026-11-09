from pathlib import Path
import hashlib
from .chunk import Chunk
import json

class Document:
    def __init__(self, name: str, path: Path, raw_text: str, keywords=None, metadata: dict = None,):
        self.name = name
        self.path = Path(path)
        self.raw_text = raw_text

        self.keywords = keywords 
        self.chunks: list[Chunk] = []
        self.metadata = metadata 

        self.id = self._generate_id()

    def add_chunk(self, chunk: Chunk):
        """
        Append Chunk object into the Document object 
        """
        chunk.document_id = self.id
        chunk.chunk_index = len(self.chunks) + 1
        chunk.id = f"{self.id}_{chunk.chunk_index}"

        self.chunks.append(chunk)
    
    def _generate_id(self) -> str:
        """
        Generates a hach ID based on the document text content, each document will be unique but always give the same ID

            Returns: doc_ + 12 symbol Hachcode
        """
        content = self.raw_text or str(self.path)
        hash_digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
        return f"doc_{hash_digest[:12]}"


    def serialize_object_data(self) -> dict:
        """
        Goes through each chunk, checks if there is a valid Vector array appends each chunk to a list.

            Returns: Dict: containing all data stored in Document
        """
        gathered_chunks = []
        for chunk in self.chunks:
            stored_vector = getattr(chunk, "vector", None)

            if stored_vector is not None and hasattr(stored_vector, "tolist"):
                valid_vector = stored_vector.tolist()
            else:
                valid_vector = stored_vector

            gathered_chunks.append({
                "id": getattr(chunk, "id", None),
                "chunk_index": getattr(chunk, "chunk_index", None),
                "document_id": getattr(chunk, "document_id", self.id),
                "text": getattr(chunk, "text", ""),
                "keywords": getattr(chunk, "keywords", []),
                "keynames": getattr(chunk, "keynames", []),
                "vector": valid_vector,
            })

        return {
            "id": self.id,
            "name": self.name,
            "path": str(self.path),
            "raw_text": self.raw_text,
            "keywords": self.keywords,
            "metadata": self.metadata,
            "chunks": gathered_chunks,
        }
    
    def save_to_json(self):
        output_folder = Path("repositories")
        out_path = Path(output_folder)
        out_path.mkdir(parents=True, exist_ok=True)

        file_destination = out_path / f"{self.id}.json"

        with open(file_destination, "w", encoding="utf-8") as f:
            json.dump(self.serialize_object_data(), f, ensure_ascii=False, indent=2)

        return file_destination
    
    def __str__(self):
        """
        Format and print data contained in Document
        """

        keyword_items = getattr(self, "keywords", []) 
        formatted_keywords = [
           ", ".join(f"{k['keyword']} ({k['score']:.4f})" 
            for k in keyword_items) or "None"
        ]

        return(
            f"Document: {self.name}, \n"
            f"ID: {self.id}, \n"
            f"Total Chunks: {len(self.chunks)}, \n" 
            f"Metadata: {self.metadata}, \n"
            f"keywords: {formatted_keywords}"
        ) 