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

    def process_query(self, query: str):
        search_query = query.strip()
        if not search_query:
            return {}

        vector_result = self._data_extractor._vectorizer.vectorize_chunks(
            [search_query]
        )
        vector = (
            vector_result[0].tolist()
            if hasattr(vector_result[0], "tolist")
            else list(vector_result[0])
        )

        yake_result = self._data_extractor._keyword_extractor.get_yake(
            [search_query]
        )
        keywords = yake_result[0] if yake_result else []

        ner_result = self._data_extractor._keyword_extractor.get_ner([search_query])

        return {
            "query": search_query,
            "keywords": keywords,
            "entities": ner_result,
            "vector": vector,
        }