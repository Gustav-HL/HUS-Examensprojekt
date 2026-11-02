from pathlib import Path
import hashlib
from chunk import Chunk


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

        chunk.document_id = self.id
        chunk.chunk_index = len(self.chunks)
        chunk.id = f"{self.id}_{chunk.chunk_index}"

        self.chunks.append(chunk)
    
    def _generate_id(self) -> str:

        content = self.raw_text or str(self.path)
        hash_digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
        return f"doc_{hash_digest[:12]}"

    def __str__(self):

        keyword_items = getattr(self, "keywords", []) 
        formatted_keywords = [
            f"{keyword['keyword']} ({keyword['score']:.4f}) "
            for keyword in keyword_items
        ]

        return(
            f"Document: {self.name}, \n"
            f"ID: {self.id}, \n"
            f"Total Chunks: {len(self.chunks)}, \n" 
            f"keywords: {formatted_keywords}, \n"
            f"Metadata: {self.metadata}"
        ) 