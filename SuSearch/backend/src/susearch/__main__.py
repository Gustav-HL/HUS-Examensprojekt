import webview
import os
import json
import tempfile
import base64
import time
import logging

from services.document_chunker import DocumentChunker
from services.keyword_extractor import KeywordExtractor
from services.file_handler import FileHandler
from pathlib import Path
from models.document import Document
from models.chunk import Chunk
from services.vector_extractor import Vectorizer
from services.cosine_similarity import cosineSimilarityCalculator
from services.file_scanner import DocumentScanner
from services.search_engine import SearchEngine
from repositories.database import LocalDataStorage

import time
import logging

logging.getLogger("pypdf").setLevel(logging.ERROR)

# Get the directory where database_test file is located
BASE_DB = Path(__file__).resolve().parent

# Create a path to the database file from repositories folder.
DB_PATH = BASE_DB / "repositories" / "HUT_DATA.db"

class DataExtractor:
    """
    
    """
    def __init__(self):
        self._keyword_extractor = KeywordExtractor(     
            lan = "sv",
            n = 2, # Amount of words per phrase
            dedupLim = 0.4, # Let duplicates
            top = 25,  # Amount of results
            features = None
        )
        self._vectorizer = Vectorizer()

    def get_chunks(self, raw_document: str, document_name: str) -> list[str]:
        chunker = DocumentChunker(raw_document, document_name)
        return chunker.chunk_document()
     
class DesktopBridge:
    """ 
    Acts as a bridge between frontend and backend.
    """
    def __init__(self, search_engine: SearchEngine, data_extractor: DataExtractor, file_scanner: DocumentScanner, database: LocalDataStorage):
        self.search_engine = search_engine
        self._window = None
        self.data_extractor = data_extractor
        self.file_scanner = file_scanner
        self.database = database

    def select_folder(self):
        if not self._window:
            return None
        result = self._window.create_file_dialog(webview.FileDialog.FOLDER)
        if not result:
            return None
        if result:
            results = result[0] 
        return str(Path(results))
    
    def handle_documents(self):
        folderP = self.select_folder()
        if not folderP:
            print("Canceled")
            return
        folder_res = self.file_scanner.scan_and_track(folderP)
        folderPath = Path(folder_res)
        print("Success")
        print(folderP)
        try:
            process_all_documents(self.data_extractor, self.file_scanner, folderPath,  self.database)
        except Exception as e:
            print(f"Error in process_all_documents: {e}")
            raise

    def search_text(self, query: str):
        query_doc = self.search_engine.process_query(query)
        if not query_doc:
            return []

        search_match, search_low = self.search_engine.search(query_doc)

        for i, item in enumerate(search_low):
            title = item.get("title") or "No Name"
            keyword_score = item.get("keyword_score", 0.0)

            matched = [
                f"{match['query_keyword']} MATCHED {match['document_keyword']} ({match['score']})"
                for match in item.get("matched_keywords", [])
            ]
            matched_ner = [
                f"{match['query_keyword']} MATCHED {match['document_keyword']} ({match['score']})"
                for match in item.get("matched_ner", [])
            ]

            print(f"{i}. {title}")
            print(f"   Total score: {item.get('score', 0.0):.4f}")
            print(f"   Keyword points: {keyword_score:.4f}")
            print(f"   Matched Keywords: {', '.join(matched) if matched else 'None'}")
            print(f"   NER points: {item.get('ner_score', 0.0):.4f}")
            print(f"   Cos score: {item.get('cos_score', 0.0):.4f}")
            print(f"   Matched NER: {', '.join(matched_ner) if matched_ner else 'None'}")

        return search_match

    def search_by_document(self, document_input):
        """
        Get the document from frontend. 
        Create a temporary file if needed.
        Process the document in same way as a search query with SearchEngine
        Remove the file
        """
        if isinstance(document_input, dict):
            if "data" in document_input:
                raw_data = document_input["data"]
                if "," in raw_data:
                    raw_data = raw_data.split(",", 1)[1]

                original_name = document_input.get("name", "upload.txt")
                suffix = Path(original_name).suffix
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(base64.b64decode(raw_data))
                    tmp_path = Path(tmp.name)

                try:
                    doc = self.search_engine.process_query_document(tmp_path)
                    if not doc:
                        return []
                    doc.name = original_name
                    doc_search, search_low = self.search_engine.search(doc)
                    
                    for i, item in enumerate(search_low):
                        title = item.get("title") or "No Name"
                        keyword_score = item.get("keyword_score", 0.0)
            
                        matched = [
                            f"{match['query_keyword']} MATCHED {match['document_keyword']} ({match['score']})"
                            for match in item.get("matched_keywords", [])
                        ]
                        matched_ner = [
                            f"{match['query_keyword']} MATCHED {match['document_keyword']} ({match['score']})"
                            for match in item.get("matched_ner", [])
                        ]

                        print(f"{i}. {title}")
                        print(f"   Total score: {item.get('score', 0.0):.4f}")
                        print(f"   Keyword points: {keyword_score:.4f}")
                        print(f"   Matched Keywords: {', '.join(matched) if matched else 'None'}")
                        print(f"   NER points: {item.get('ner_score', 0.0):.4f}")
                        print(f"   Cos score: {item.get('cos_score', 0.0):.4f}")
                        print(f"   Matched NER: {', '.join(matched_ner) if matched_ner else 'None'}")

                    return doc_search
                
                finally:
                    if tmp_path.exists():
                        tmp_path.unlink()

            target_path = (
                document_input.get("path")
                or document_input.get("filePath")
                or document_input.get("name")
            )
        else:
            target_path = document_input

        if not target_path:
            return {"error": "Ingen giltig sökväg mottogs."}

        path = Path(target_path)
        if not path.is_file():
            return {"error": f"Filen hittades inte: {path}"}

        doc = self.search_engine.process_query_document(path)
        if not doc:
            return []
        
        doc.name = path.name
        return self.search_engine.search(doc)

# C:\Users\leona\OneDrive

def process_all_documents(data_extractor: DataExtractor, file_scanner: DocumentScanner, folder: Path, database: LocalDataStorage):
    total_start = time.perf_counter()
    file_handler = FileHandler()
    folder_data = file_scanner.fetch_data()

    for file_path, file_info in folder_data.get("files", {}).items():
        if not file_info['name'].endswith(('.pdf', '.docx', '.txt')) or not file_path.endswith(('.pdf', '.docx', '.txt')):
            continue

        try:
            print(f"\nName: {file_info['name']}")
            name = file_info["name"]
            file_full_path = folder / file_path
            
            with open(BASE_DB/"services/file_tracker.json", "r", encoding="utf-8") as file:
                data = json.load(file)

            #     file_record = data.get("files", {}).get(file_path, {})

            # if file_record.get("state") is not True:
            #     print(f"Skipping {file_info['name']}")
            #     continue

            t0 = time.perf_counter()
            raw_text = file_handler.extract_text(file_full_path)
            t_extract = time.perf_counter() - t0

            if raw_text:
                path = file_full_path
                document = file_handler.extract_text(path)
                metadata = file_handler.extract_metadata(path)

                _keyword_extractor = data_extractor._keyword_extractor
                format_yake = _keyword_extractor.get_yake([document])
                full_yake = format_yake[0] if format_yake else []

                doc = Document(name=name, path=path, raw_text=document, keywords=full_yake, metadata=metadata)
                chunks = data_extractor.get_chunks(raw_text, file_info["name"])

                yake_results = [[] for _ in chunks]
                ner_results = _keyword_extractor.get_ner(chunks)

                _vectorizer = data_extractor._vectorizer
                vector_result = _vectorizer.vectorize_chunks(chunks)

                for index, (chunk, keywords, ner, vector) in enumerate(zip(chunks, yake_results, ner_results, vector_result), start=1):
                    #print(f"Chunk {index}")
                    ultimate_chunk = Chunk(text=chunk, source=name, keywords=keywords, keynames=ner, vector=vector )
                    doc.add_chunk(ultimate_chunk)
                    #print(ultimate_chunk)

                #print(doc)
                database.save_document(doc)
                # Send document object to database
                # database.test_database(doc)
            else:
                print("Skipped (No text found or unsupported format).")
        except Exception as e:
            print(f"Error processing file: {e}")
    

def process_document(data_extractor: DataExtractor, file_scanner: DocumentScanner, folder: Path, name: str, database: LocalDataStorage):
    file_handler = FileHandler()
    
    find_path = None
    for root, dirs, files in os.walk(folder):
        if name in files:
            find_path = os.path.join(root, name)
            break

    if find_path:
        document = file_handler.extract_text(find_path)
        metadata = file_handler.extract_metadata(find_path)

        _keyword_extractor = data_extractor._keyword_extractor

        format_yake = _keyword_extractor.get_yake([document])
        full_yake = format_yake[0] if format_yake else []

        doc = Document(name=name, path=find_path, raw_text=document, keywords=full_yake, metadata=metadata)

        chunks = data_extractor.get_chunks(document, name)

        # _keyword_extractor = KeywordExtractor()
        # yake_results = _keyword_extractor.get_yake(chunks) # Disabled atm to test whole document keywords

        yake_results = [[] for _ in chunks]
        ner_results = _keyword_extractor.get_ner(chunks)

        _vectorizer = data_extractor._vectorizer
        vector_result = _vectorizer.vectorize_chunks(chunks)

        #Testar calculate i cosine similarity calculator
        query = ["Region Skånes Miljövårdsfond stödjer idéer som kan bidra till ett miljömässigt hållbart Skåne i synergi med övriga hållbarhetsaspekter (ekonomiska och sociala). Beviljade projekt är av utvecklingskaraktär och ska stödja den regionala utvecklingsstrategin ”Det Öppna Skåne 2030”, ”Regionalt åtgärdsprogram för miljömålen”, samt ”Klimat- och energistrategin för Skåne Design and Creation fallstudie”."]
        query_vector = _vectorizer.vectorize(query)
        calculator = cosineSimilarityCalculator()
        cosine_results = calculator.calculateStrings(query_vector, vector_result)

        for index, (chunk, keywords, ner, vector) in enumerate(zip(chunks, yake_results, ner_results, vector_result), start=1):
            # print(f"Chunk {index}")
            ultimate_chunk = Chunk(text=chunk, source=name, keywords=keywords, keynames=ner, vector=vector )

            doc.add_chunk(ultimate_chunk)
            # print(ultimate_chunk)

        print("COSINE RESULTS:")
        for index, score in cosine_results.items():
            print(f"{index}: {score:.4f}")

        saved_file = doc.save_to_json()
        database.save_document(doc)
        documents = database.get_document_data()
        print(json.dumps(documents, ensure_ascii=False, indent=2))

        # Send document object to database
        # database.test_database(doc)
    else:
        print(f"File {name} not found in {folder}\n :(")

if __name__ == "__main__":
    data_extractor = DataExtractor()
    file_scanner = DocumentScanner()
    database = LocalDataStorage(DB_PATH)
    
    search_engine = SearchEngine(data_extractor, database)

    start_view = input("Start in react? \n   1.No\n   2.Yes (You need to have npm running'.\Start.ps1') \n 3. Amelies test thing \n")
    if start_view == "1":
        print("Started  terminal")
        folder_input = input("Choose folder: ") # C:\Users\leona\OneDrive
        current_dir = Path(__file__).resolve().parent
        folder_res = (
            file_scanner.scan_and_track(folder_input)
            if folder_input
            else file_scanner.scan_and_track(str(current_dir))
        )
        folder = Path(folder_res)
        name = input("Enter file name and file suffix(Kan köra All Files för att chunka allt(OBS vet inte om det fungerar 100% gör det på egen risk)): ")

        if name.lower() == "all files":
            process_all_documents(data_extractor, file_scanner, folder,  database)
        else:
            process_document(data_extractor, file_scanner, folder, name, database)

    elif start_view == "2":
        bridge = DesktopBridge(search_engine, data_extractor, file_scanner, database)
        window = webview.create_window(
            title="SuSearch",
            url="http://localhost:5173",
            js_api=bridge
        )
        bridge._window = window

        webview.start(
            debug=True,
            private_mode=False
        )

    elif start_view == "3":
        print("Started terminal")
        #Find folder to extract documents from
        folder_input = input("Choose folder to insert documents from: ")
        current_dir = Path(__file__).resolve().parent
        folder_res = (
            file_scanner.scan_and_track(folder_input)
            if folder_input
            else file_scanner.scan_and_track(str(current_dir))
        )
        folder = Path(folder_res)

        #Inserts documents into database
        process_all_documents(data_extractor, file_scanner, folder,  database)

        calculator = cosineSimilarityCalculator()

        #Test query is vectorized
        query = ["Region Skånes Miljövårdsfond stödjer idéer som kan bidra till ett miljömässigt hållbart Skåne i synergi med övriga hållbarhetsaspekter (ekonomiska och sociala). Beviljade projekt är av utvecklingskaraktär och ska stödja den regionala utvecklingsstrategin ”Det Öppna Skåne 2030”, ”Regionalt åtgärdsprogram för miljömålen”, samt ”Klimat- och energistrategin för Skåne”."]
        query_vector = data_extractor._vectorizer.vectorize(query)

        #Fetch vectors of all chunks in the database
        chunk_vectors = database.get_all_chunk_vectors()

        #Calculate cosine similarity with the vector of the query and the vectors of all chunks
        cosine_results = calculator.calculateStrings(query_vector, chunk_vectors)

        #Map each chunk to the name of its document
        chunk_to_name = database.get_document_names_for_chunks(list(cosine_results.keys()))

        #cosine_results is sorted best first, so each document gets its best score
        printed = set()
        match_number = 1
        for chunk_id, score in cosine_results.items():
            name = chunk_to_name.get(chunk_id)
            if name is None or name in printed:
                continue
            printed.add(name)
            print(f"{match_number}. {name}")
            match_number += 1
            print()

    elif start_view == "4":
        rows = database.get_document_data()

        docs = [
            {
                "doc_id": row["id"],
                "title": row["name"],
                "file_path": row["path"],
                "keywords": row.get("keywords") or [],
            }
            for row in rows
        ]

        with open("documents.json", "w", encoding="utf-8") as f:
            json.dump(docs, f, ensure_ascii=False, indent=2)

    else:
        print("Wrong Choice Buddy")