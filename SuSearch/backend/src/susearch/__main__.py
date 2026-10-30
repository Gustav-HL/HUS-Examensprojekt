import webview
from models.document_chunker import DocumentChunker
from services.keyword_extractor import KeywordExtractor
from services.file_handler import FileHandler
from pathlib import Path
from models.chunk import Chunk
from services.testing_kblab import Vectorizer

class DataExtractor:
    """
    
    """
    def __init__(self):
        self._keyword_extractor = KeywordExtractor()
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



def process_document(data_extractor: DataExtractor):

    file_handler = FileHandler()
    current_dir = Path(__file__).resolve().parent

    folder_input = input("Choose folder: ") 
    folder = Path(folder_input) if folder_input else current_dir 

    name = input("Enter file name and file suffix: ")
    path = folder / name
    document = file_handler.extract_text(path)

    chunks = data_extractor.get_chunks(document, name)
    # _keyword_extractor = KeywordExtractor()

    _keyword_extractor = data_extractor._keyword_extractor
    yake_results = _keyword_extractor.get_yake(chunks)
    ner_results = _keyword_extractor.get_ner(chunks)

    print(f"\nAmount of chunks: {len(chunks)}")
    
    _vectorizer = data_extractor._vectorizer
    # _vectorizer = _Vectorizer()
    vector_result = _vectorizer.vectorize_chunks(chunks)

    for index, (chunk, keywords, ner, vector) in enumerate(zip(chunks, yake_results, ner_results, vector_result), start=1):
        print(f"Chunk {index} YAKE words")
        # print(chunk)
        ultimate_chunk = Chunk(text=chunk, source=name, keywords=keywords, keynames=ner, vector=vector)

        # for item in keywords:
        #     print(f"   {item['keyword']} (score: {item['score']})")

        # print(" ")
        # print(f"Chunk {index} NER words")
        # for ent in ner:
        #         print(f"   {ent['word']} ({ent['entity_group']}, score: {ent['score']})")

        # print("\n" + " " * 20  + "\n")
        print(ultimate_chunk)


if __name__ == '__main__':
    data_extractor = DataExtractor()

    process_document(data_extractor)

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
