from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline
import yake

class KeywordExtractor:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("KBLab/bert-base-swedish-cased-ner")
        self.model = AutoModelForTokenClassification.from_pretrained(
            "KBLab/bert-base-swedish-cased-ner"
        )

        self.ner = pipeline(
            "ner",
            model = self.model,
            tokenizer = self.tokenizer,
            aggregation_strategy = "simple",  # Combines part words to whole words
        )
        self._kw_extractor = yake.KeywordExtractor(
            lan = "sv",
            n = 3,
            dedupLim = 0.4,
            top = 10,
            features = None
        )

    def get_NER(self):
        ner_results = self.ner(self.document_chunks)
        return ner_results

    def get_yake(self, chunks: list[str]) -> list[list[dict]]:
        results = []
        for chunk in chunks:
            if not chunk or not chunk.strip():
                results.append([])
                continue
            
            # YAKE operates on individual text strings
            keywords = self._kw_extractor.extract_keywords(chunk)
            results.append([
                {"keyword": kw, "score": round(float(score), 4)}
                for kw, score in keywords
            ])
        return results