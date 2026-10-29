import webview
from models.document_chunker import DocumentChunker
from services.keyword_extractor import KeywordExtractor
from services.file_handler import FileHandler
from pathlib import Path

class DataExtractor:
    """
    
    """
    def __init__(self, raw_document: str):
        self._chunker = DocumentChunker(raw_document)
        
        self.chunks = self._chunker.chunk_document()
        
        self._embedding_service = None
        self._keyword_service = None

    def get_chunks(self) -> list[str]:
        return self.chunks
    
class DesktopBridge:
    """ 
    Acts as a bridge between frontend and backend.
    """
    def __init__(self, data_extractor: DataExtractor):
        self._data_extractor = data_extractor
        self._window = None 
    
    def execute_search(self, query: str):
        return self._data_extractor.search(query)

file_handler = FileHandler()
folder = Path(input("Choose folder: "))
name = input("Enter file name and file suffix: ")
path = folder / name
document = file_handler.extract_text(path)

if __name__ == '__main__':
    data_extractor = DataExtractor(document)
    chunks = data_extractor.get_chunks()

    keyword_extractor = KeywordExtractor()
    yake_results = keyword_extractor.get_yake(chunks)
    ner_results = keyword_extractor.get_ner(chunks)

    print(f"\nAmount of chunks: {len(chunks)}")
    
    for index, (chunk, keywords, ner) in enumerate(zip(chunks, yake_results, ner_results), start=1):

        print(f"Chunk {index} YAKE words")
        print(chunk)
        for item in keywords:
            print(f"   {item['keyword']} (score: {item['score']})")

        print(" ")
        print(f"Chunk {index} NER words")
        for ent in ner:
                print(f"   {ent['word']} ({ent['entity_group']}, score: {ent['score']})")

        print("\n" + " " * 20  + "\n")


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
