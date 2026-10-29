from langchain_text_splitters import RecursiveCharacterTextSplitter
from SuSearch.backend.src.susearch.services.file_handler import fileHandler
from pathlib import Path

class Chunker:
    def __init__(self):
        pass

    file_handler = fileHandler()
    
    folder = Path(r"C:\Users\ameli\Kurser\DA223E\Lectures")
    path = folder / "Lecture 9_Access Control.pdf"
    text = file_handler.extract_text(path)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1500,
        chunk_overlap = 250,
        length_function = len,
    )

    chunks = text_splitter.split_text(text)
    index = 0

    for i, chunk in enumerate(chunks):
        print("-----CHUNK NUMBER", i, f"({len(chunk)} tecken)-----")
        print(chunk)
        print(" " * 40)

    import yake

    kw_extractor = yake.KeywordExtractor(
        lan="sv", 
        n=3,              
        dedupLim=0.4,     
        top=15
    )

    print("KEYWORDS:")
    keywords = kw_extractor.extract_keywords(chunks[0])
    for kw, score in keywords:
        print(f"{kw} ({score:.4f})")