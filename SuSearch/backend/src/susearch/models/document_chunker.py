from langchain_text_splitters import RecursiveCharacterTextSplitter
import yake
from models.chunk import Chunk

class DocumentChunker:
    def __init__(self, raw_text: str, document_name: str):
        self.raw_text = raw_text
        self.document_name = document_name
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1500,
            chunk_overlap= 250,
            length_function = len,
        )

    def chunk_document(self) -> list[Chunk]:
        return self.text_splitter.split_text(self.raw_text) 
