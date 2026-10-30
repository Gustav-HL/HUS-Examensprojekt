class Chunk:
    def __init__(self, text: str, source: str, keywords: list[str], keynames, vector):
        self.text = text
        self.source = source
        self.keywords = keywords
        self.keynames = keynames
        self.vector = vector

    def __str__(self):


        ner_items = getattr(self, "keynames", []) 
        formatted_ner = [
            f"{e['word']} ({e.get('entity_group', '')}) "
            for e in ner_items
        ]

        keyword_items = getattr(self, "keywords", []) 
        formatted_keywords = [
            f"{k['keyword']} ({k['score']:.4f}) "
            for k in keyword_items
        ]

        return (
            f"text: {self.text}, "
            f"source: {self.source}, \n"
            f"keywords: {formatted_keywords}, \n"
            f"ner: {formatted_ner}, \n"
            f"vector: {self.vector}"
        )

    