from pathlib import Path
from .file_handler import FileHandler
from models.document import Document
from models.chunk import Chunk


class SearchEngine:
    def __init__(self, data_extractor):
        self._data_extractor = data_extractor
        self._file_handler = FileHandler()

    def _process_text(self, text: str, source_name: str, file_path: Path | None = None) -> Document:
        yake_result = self._data_extractor._keyword_extractor.get_yake([text])
        keywords = yake_result[0] if yake_result else []
        metadata = self._file_handler.extract_metadata(file_path) if file_path else {}

        doc = Document(
            name=source_name,
            path=file_path if file_path else Path(source_name),
            raw_text=text,
            keywords=keywords,
            metadata=metadata,
        )

        chunks = self._data_extractor.get_chunks(text, source_name)
        if not chunks:
            chunks = [text]

        ner_result = self._data_extractor._keyword_extractor.get_ner(chunks)
        vector_result = self._data_extractor._vectorizer.vectorize_chunks(chunks)

        for chunk, ner, vec in zip(chunks, ner_result, vector_result):
            if hasattr(vec, "detach"):
                vec = vec.detach().cpu()

            ultimate_chunk = Chunk(
                text=chunk,
                source=source_name,
                keywords=[],
                keynames=ner,
                vector=vec,
            )
            doc.add_chunk(ultimate_chunk)

        return doc

    def process_query_document(self, file_path: Path) -> Document:
        """
        Extract text, chunk the document and generate vectors for each chunk

            Args: Path(str): The filepath
            Returns: Document: A Document object containing extracted data
        """
        document = self._file_handler.extract_text(file_path)
        
        processed_doc = self._process_text(document, file_path.name, file_path=file_path)
        print("Query Processed")
        return processed_doc

    def process_query(self, query: str) -> Document:
        """
        Process a text query into vectors, keywords and NER

            Args: query(str): The text query entered by user
            Returns: Document: A Document object containing extracted data
        """
        search_query = query.strip()

        processed_query = self._process_text(search_query, "query_text")
        print("Document Processed")
        return processed_query