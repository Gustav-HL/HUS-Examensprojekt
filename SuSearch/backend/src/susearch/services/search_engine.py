from pathlib import Path
from .file_handler import FileHandler


class SearchEngine:
    def __init__(self, data_extractor):
        self._data_extractor = data_extractor
        self._file_handler = FileHandler()

    def _to_clean_list(self, vec):
        if hasattr(vec, "detach"):
            vec = vec.detach().cpu()
        return vec.tolist() if hasattr(vec, "tolist") else list(vec)

    def _process_text(self, text: str, source_name: str) -> dict:
        yake_result = self._data_extractor._keyword_extractor.get_yake([text])
        keywords = yake_result[0] if yake_result else []

        chunks = self._data_extractor.get_chunks(text, source_name)
        if not chunks:
            chunks = [text]

        ner_result = self._data_extractor._keyword_extractor.get_ner(chunks)
        vector_result = self._data_extractor._vectorizer.vectorize_chunks(chunks)

        processed_chunks = []
        for chunk, ner, vec in zip(chunks, ner_result, vector_result):
            processed_chunks.append({
                "text": chunk,
                "source": source_name,
                "keynames": ner,
                "vector": self._to_clean_list(vec),
            })

        return {
            "source": source_name,
            "keywords": keywords,
            "chunks": processed_chunks,
        }

    def process_query_document(self, file_path: Path) -> dict:
        """
        Extract text, chunk the document and generate vectors for each chunk.

            Args: Path(str): The filepath
            Returns: Dict: A dictionary contaiting data extracted
        """
        document = self._file_handler.extract_text(file_path)
        if not document:
            return {}

        print("document processed")
        document = self._process_text(document, file_path.name)
        print(document)
        return document

    def process_query(self, query: str) -> dict:
        """
        Process a text query into its vector, keywords, and NER entities.

            Args: query(str): The text query entered by user
            Returns: Dict: A dictionary contaiting data extracted
        """
        search_query = query.strip()
        if not search_query:
            return {}

        result = self._process_text(search_query, "query_text")
        result["query"] = search_query
        print("query processed")
        return result