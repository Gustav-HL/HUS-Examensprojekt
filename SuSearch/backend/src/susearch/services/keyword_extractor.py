from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline
import yake

class KeywordExtractor:
    """
    Extracts entities such as names, locations and time. Aswell as words and phrases.
    """
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("KBLab/bert-base-swedish-cased-ner")
        self.model = AutoModelForTokenClassification.from_pretrained(
            "KBLab/bert-base-swedish-cased-ner"
        )

        self._ner = pipeline(
            "ner",
            model = self.model,
            tokenizer = self.tokenizer,
            aggregation_strategy = "simple",  # Combines part words to whole words
        )

        self._keyword_yake = yake.KeywordExtractor(
            lan = "sv",
            n = 1, # Amount of words per phrase
            dedupLim = 0.4, # Let duplicates
            top = 15,  # Amount of results
            features = None
        )

    def get_ner(self, chunks: list[str]) -> list[list[dict]]:
        """
        Run a chunk of text through NER model and return the resultning enteties
            Args:
                chunks: a list of strings representing chunks of a document

            Returns:
                List: dictionary representing a single entity found, inside a list inside a list
        """
        raw_results = self._ner(chunks, batch_size=8)
        print(raw_results)
        results = []

        for chunk_entities in raw_results:
            cleaned_entities = []

            for ent in chunk_entities:

                cleaned_entities.append({
                    "entity_group": ent["entity_group"],
                    "word": ent["word"].strip(),
                    "score": round(float(ent["score"]), 4)
                })
                
            results.append(cleaned_entities)

        return results
    

    def get_yake(self, chunks: list[str]) -> list[list[dict]]:
        """
        Run a chunk of text through YAKE model and return the resultning words or phrases
            Args:
                chunks: a list of strings representing chunks of a document

            Returns:
                List: dictionary containing keyword and score(lower means better with YAKE), inside a list inside a list
        """
        results = []

        for chunk in chunks:
            if not chunk or not chunk.strip():
                results.append([])
                continue
            
            keywords = self._keyword_yake.extract_keywords(chunk)

            results.append([
                {"keyword": keyword, "score": round(float(score), 4)}
                for keyword, score in keywords
            ])

        return results