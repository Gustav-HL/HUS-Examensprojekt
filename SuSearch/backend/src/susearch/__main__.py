import webview
import os
from models.document_chunker import DocumentChunker
from services.keyword_extractor import KeywordExtractor
from services.file_handler import FileHandler
from pathlib import Path
from models.document import Document
from models.chunk import Chunk
from services.testing_kblab import Vectorizer

from services.file_scanner import DocumentScanner
from services.search_engine import SearchEngine

class DataExtractor:
    """
    
    """
    def __init__(self):
        self._keyword_extractor = KeywordExtractor(     
                    lan = "sv",
                    n = 3, # Amount of words per phrase
                    dedupLim = 0.4, # Let duplicates
                    top = 30,  # Amount of results
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
    def __init__(self, data_extractor: DataExtractor):
        self._data_extractor = data_extractor
        self._window = None 
    
    def execute_search(self, query: str):
        return self._data_extractor.search(query)



def process_all_documents(data_extractor: DataExtractor, file_scanner: DocumentScanner, folder: Path):
    file_handler = FileHandler()
    folder_data = file_scanner.fetch_data()

    for file_path, file_info in folder_data.get("files", {}).items():
        if not file_info['name'].endswith(('.pdf', '.docx', '.txt')) or not file_path.endswith(('.pdf', '.docx', '.txt')):
            continue

        try:
            print(f"\nName: {file_info['name']}")
            file_full_path = folder / file_path
            raw_text = file_handler.extract_text(file_full_path)

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
                    print(f"Chunk {index} YAKE words")
                    ultimate_chunk = Chunk(text=chunk, source=name, keywords=keywords, keynames=ner, vector=vector )
                    doc.add_chunk(ultimate_chunk)
                    print(ultimate_chunk)

                print(doc)
            else:
                print("Skipped (No text found or unsupported format).")
        except Exception as e:
            print(f"Error processing file: {e}")


def process_document(data_extractor: DataExtractor, file_scanner: DocumentScanner, folder: Path, name: str,):
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
        yake_results = [[] for _ in chunks]
        ner_results = _keyword_extractor.get_ner(chunks)

        _vectorizer = data_extractor._vectorizer
        vector_result = _vectorizer.vectorize_chunks(chunks)

        for index, (chunk, keywords, ner, vector) in enumerate(zip(chunks, yake_results, ner_results, vector_result), start=1):
            print(f"Chunk {index} YAKE words")
            ultimate_chunk = Chunk(text=chunk, source=name, keywords=keywords, keynames=ner, vector=vector )

            doc.add_chunk(ultimate_chunk)
            print(ultimate_chunk)

        print(doc)
    else:
        print(f"File {name} not found in {folder}\n :(")

def search(search_engine: SearchEngine):
    current_dir = Path(__file__).resolve().parent

    folder_input = input("Choose folder: ")
    folder = Path(folder_input) if folder_input else current_dir

    name = input("Enter file name and file suffix: ")
    path = folder / name

    query_data = search_engine.process_query_document(path)

    for index, (chunk_text, vector) in enumerate(query_data, start=1):
        print(f"Chunk {index}")
        print(chunk_text)
        print(vector)


if __name__ == "__main__":
    data_extractor = DataExtractor()
    file_scanner = DocumentScanner()
    search_engine = SearchEngine(data_extractor)

    choice = input("1. Search \n2. Scan \n")
    if choice == "1":
        search(search_engine)

    elif choice == "2":
        folder_input = input("Choose folder: ")
        current_dir = Path(__file__).resolve().parent
        folder_res = (
            file_scanner.scan_and_track(folder_input)
            if folder_input
            else file_scanner.scan_and_track(str(current_dir))
        )
        folder = Path(folder_res)

        name = input("Enter file name and file suffix(Kan köra All Files för att chunka allt(OBS vet inte om det fungerar 100% gör det på egen risk)): ")

        if name.lower() == "all files":
            process_all_documents(data_extractor, file_scanner, folder)
        else:
            process_document(data_extractor, file_scanner, folder, name)

    else:
        print("Wrong Choice Buddy")

    # bridge = DesktopBridge(data_extractor)


    # window = webview.create_window(
    #     title="SuSearch",
    #     url="http://localhost:5173",
    #     js_api=bridge
    # )

    # def on_closing():
    #         print("Closing start cleanup.")
    #         data_extractor.cleanup()

    # window.events.closing += on_closing

    # webview.start(debug=True)
