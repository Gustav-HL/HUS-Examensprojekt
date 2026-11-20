from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline
import yake
from services.word_score import wordScorer

# Words that will be excluded by YAKE in keyword generation
STOPWORDS = {
    "och", "att", "det", "som", "för", "med", "till", "den", "samt",
    "ska", "skall", "kan", "har", "hade", "var", "är", "ett", "en",
    "på", "av", "om", "men", "inte", "eller", "från", "vid", "inom",
    "över", "under", "genom", "mellan", "mot", "hos", "ut", "upp",
    "sig", "sin", "sitt", "sina", "vi", "ni", "de", "dem", "deras",
    "vår", "vårt", "våra", "denna", "detta", "dessa", "här", "där",
    "när", "hur", "vad", "vilken", "vilket", "vilka", "alla", "andra",
    "olika", "även", "också", "dock", "bara", "mer", "mest", "mycket",
    "oss", "vem", "stad", "skåne", "region", "gäller", "dokument",
    "orginal", "dokumentid", "gällande", "projekt", "ange",
    "medel", "version"

    "and", "the", "for", "with", "that", "this", "from", "are", "was",
    "were", "been", "have", "has", "had", "will", "would", "could",
    "should", "can", "may", "might", "not", "but", "what", "all",
    "when", "where", "which", "who", "how", "why", "into", "than",
    "then", "there", "their", "they", "them", "these", "those", "its",
    "our", "your", "more", "most", "other", "some", "such", "only",
    "also", "very", "just", "about", "over", "after", "before", "between",
}

class KeywordExtractor:
    """
    Extracts entities such as names, locations and time. Aswell as words and phrases.
    """
    def __init__(self, lan, n, dedupLim, top, features):
        self.tokenizer = AutoTokenizer.from_pretrained("KBLab/bert-base-swedish-cased-ner")
        self.tokenizer.model_max_length = 512
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
            lan = lan,
            n = n, 
            dedupLim = dedupLim, 
            top = top,  
            features = features,
            stopwords = STOPWORDS
        )

    def get_ner(self, chunks: list[str]) -> list[list[dict]]:
        """
        Run a chunk of text through NER model and return the resultning enteties
            Args:
                chunks: a list of strings representing chunks of a document

            Returns:
                List: dictionary representing a single entity found, inside a list inside a list
        """
        word_scorer = wordScorer()
        raw_results = self._ner(chunks, batch_size=8)
        # print(raw_results)
        results = []
        ALLOWED_TYPES = {"ORG", "PER", "LOC"}

        for chunk_entities in raw_results:
            cleaned_entities = []
            seen = set()

            for ent in chunk_entities:
                word = ent.get("word", "").strip()
                if ent["entity_group"] not in ALLOWED_TYPES:
                    continue

                dedup_key = word.lower()
                if dedup_key not in seen:
                    seen.add(dedup_key)
                    cleaned_entities.append({
                        "entity_group": ent["entity_group"],
                        "word": ent["word"].strip(),
                        "score": round(float(ent["score"]), 4),
                        "relevance_score": word_scorer.get_score(chunks, word)
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
        word_scorer = wordScorer()
        results = []

        for chunk in chunks:
            if not chunk or not chunk.strip():
                results.append([])
                continue
            
            keywords = self._keyword_yake.extract_keywords(chunk)

            results.append([
                {
                    "keyword": keyword.strip().lower(),
                    "relevance_score": word_scorer.get_score(chunks, keyword),
                }
                for keyword, _ in keywords
            ])

        return results