from difflib import SequenceMatcher

class KeywordMatcher:
    """
    Checks keyword matching by checking string character overlap/similarity of search query and stored database documents
    """
    def __init__(self, document_list: list, fuzzy_match_limit: float = 0.75):
        self.document_list = document_list
        self.fuzzy_match_limit = fuzzy_match_limit

    def score_keywords(self, query_keywords: list, document_keywords: list, key_name: str = "keyword"):
        """ 
        Loop through keywords from query and documents check for perfect matches, it not a perfect match check the ratio of matching characters.

            Args:
                query_keywords (list): The search query keywords
                document_keywords (list): The document keywords
            Returns:
                float: average score from keywords matching
                dict: the Mached keywords and the matching score for each word
        """
        if not query_keywords or not document_keywords:
            return 0.0, []

        total_score = 0.0
        matched_keywords = []

        # relevance_score = doc_item.get("relevance_score", 0.0)
        # relevance = 1.0 + relevance_score * 3

        # print(relevance)


        for query_item in query_keywords:
            query_keyword = query_item[key_name].strip().lower()
            match = 0.0
            match_document_keywords = None
            
            for doc_item in document_keywords:
                document_keyword = doc_item[key_name].strip().lower()
                # print(document_keyword)
                if query_keyword == document_keyword:
                    match = 1.0
                    match_document_keywords = doc_item[key_name]
                    break

                ratio = SequenceMatcher(None, query_keyword, document_keyword).ratio()
                if ratio >= self.fuzzy_match_limit and ratio > match:
                    match = ratio
                    match_document_keywords = document_keyword

                    # print(match_document_keywords, document_keyword )

            total_score += match
            if match_document_keywords:
                matched_keywords.append({
                    "query_keyword": query_item[key_name],
                    "document_keyword": match_document_keywords,
                    "score": round(match, 3),
                })

        return round(total_score / len(query_keywords), 4), matched_keywords

    def score_ner_chunks(self, query_ner: list, doc_chunks_ner: list[list]):
        """
        Combine chunk NER entities for one document and score against query NER
        
        """
        if not query_ner or not doc_chunks_ner:
            return 0.0, []

        combine_document_ner = [entity for chunk in doc_chunks_ner if chunk for entity in chunk]
        if not combine_document_ner:
            return 0.0, []

        return self.score_keywords(query_ner, combine_document_ner, key_name="word")
    
    def match(self, query_keywords: list) -> list[dict]:
        """
        Loop through the list of keywords use the score_keywords() function to find and score the matches 

            Args:
                query_keywords (list): The search query keywords
            Returns:
                List of dicts: The resulting maches and the general match score
        """
        results = []

        for document_keywords in self.document_list:
            score, matched_keywords = self.score_keywords(query_keywords, document_keywords)

            results.append({
                "score": score,
                "matched_keywords": matched_keywords,
            })

            # print(results)

        return results