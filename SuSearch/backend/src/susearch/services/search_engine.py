from pathlib import Path
from .file_handler import FileHandler


class SearchEngine:

    def __init__(self, data_extractor):
        self._data_extractor = data_extractor
        self._file_handler = FileHandler()

    def process_query_document(self, file_path: Path):
        document = self._file_handler.extract_text(file_path)
        if not document:
            return []

        chunks = self._data_extractor.get_chunks(document, file_path.name)
        if not chunks:
            return []

        vectors = self._data_extractor._vectorizer.vectorize_chunks(chunks)
        return list(zip(chunks, vectors))