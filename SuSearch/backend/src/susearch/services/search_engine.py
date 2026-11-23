import json
from pathlib import Path
from .file_handler import FileHandler
from .keyword_matcher import KeywordMatcher
from models.document import Document
from models.chunk import Chunk


class SearchEngine:
    def __init__(self, data_extractor, database):
        self._data_extractor = data_extractor
        self._file_handler = FileHandler()
        self._database = database

    def process_text(self, text: str, source_name: str, file_path: Path | None = None) -> Document:
        """
        Extract data from a text using the diffrent data extraction functions: DocumentChunker, KeywordExtractir, Vectorizer. 
        Creates Chunk and Document objects 
            Args:
                text (str): The text from a document
                source_name (str): 
                file_path: Either a file path or None depenting on if the search source is a File or Search with search bar

            Results:
                Document: Document
        """
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

            Args: 
                Path(str): The filepath
            Returns: 
                Document: A Document object containing extracted data
        """
        document = self._file_handler.extract_text(file_path)
        
        processed_doc = self.process_text(document, file_path.name, file_path=file_path)
        print("Document Processed")
        return processed_doc

    def process_query(self, query: str) -> Document:
        """
        Process a text query into vectors, keywords and NER

            Args: 
                query(str): The text query entered by user
            Returns: 
                Document: A Document object containing extracted data
        """
        search_query = query.strip()

        processed_query = self.process_text(search_query, "query_text")
        print("Query Processed")
        return processed_query


    def search(self, search_query_or_document: Document, return_amount = 10):
        """
        Match a processed query against stored documents in the database

            Args:
                search_query_or_document: Document
                return_amount (int): Max amount of documents to return
            Returns:
                Dict: A dictionary with the resulting matchning words or entities with scores based on matches
        """
        if not search_query_or_document:
            return []

        documents_from_db = self._database.get_document_data()
        ner_from_document_db = self._database.get_all_document_ner()
        
        if not documents_from_db:
            return []

        db_keywords_list = [
            json.loads(row[-1]) if isinstance(row[-1], str) and row[-1].strip() else []
            for row in documents_from_db
        ]

        query_ner = [
            entity
            for chunk in getattr(search_query_or_document, "chunks", [])
            for entity in getattr(chunk, "keynames", [])
        ]

        # Due to NER not recognizing lower case names if there are no NER entities use keywords instead 
        # Hopefully this is only used in short search queries with names
        effective_query_ner = query_ner or [
            {"word": kw["keyword"]} for kw in search_query_or_document.keywords
        ]

        matcher = KeywordMatcher(db_keywords_list)
        keyword_results = matcher.match(search_query_or_document.keywords)

        ranked_results = []
        for doc_row, keyword_result in zip(documents_from_db, keyword_results):

            keyword_score = keyword_result["score"]

            doc_ner_chunks = ner_from_document_db.get(doc_row[0], [])

            has_doc_ner = any(bool(chunk) for chunk in doc_ner_chunks)

            # check if there is NER entities in the query and the db document
            if effective_query_ner and has_doc_ner:
                ner_score, matched_ner = matcher.score_ner_chunks(effective_query_ner, doc_ner_chunks)
                total_score = round((keyword_score + ner_score) / 2, 4)

            else:
                ner_score, matched_ner = 0.0, []
                total_score = keyword_score

            ranked_results.append({
                "doc_id": doc_row[0],
                "title": doc_row[1],
                "file_path": doc_row[2],
                "score": total_score,
                "keyword_score": keyword_score,
                "ner_score": ner_score,
                "matched_keywords": keyword_result["matched_keywords"],
                "matched_ner": matched_ner,
            })

        # sort by score from match
        ranked_results.sort(key=lambda x: x["score"], reverse=True)
        return ranked_results[:return_amount]