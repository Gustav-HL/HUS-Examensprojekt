from langchain_text_splitters import RecursiveCharacterTextSplitter
import yake

class DocumentChunker:
    def __init__(self, raw_text: str):
        self.raw_text = raw_text
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1500,
            chunk_overlap= 250,
            length_function = len,
        )
        self.extractor = yake.KeywordExtractor(
        lan = "sv", 
        n = 3,              
        dedupLim = 0.4,     
        top = 15
    )


    def chunk_document(self) -> list[str]:
        if not self.raw_text:
            return []
        return self.text_splitter.split_text(self.raw_text)

    def extract_keywords_from_chunk(self, chunk: str) -> list[tuple[str, float]]:
        return self.kw_extractor.extract_keywords(chunk)