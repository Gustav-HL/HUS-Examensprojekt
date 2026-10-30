class Chunk:
    def __init__(self, text: str, source: str, keywords: list[str], keynames: list[dict], vector: list[float], id: str = None):
        self.text = text
        self.source = source
        self.keywords = keywords
        self.keynames = keynames
        self.vector = vector
        self.id = id

    def __str__(self):

        ner_items = getattr(self, "keynames", []) 
        formatted_ner = [
            f"{entity['word']} ({entity.get('entity_group', '')}) "
            for entity in ner_items
        ]

        keyword_items = getattr(self, "keywords", []) 
        formatted_keywords = [
            f"{keyword['keyword']} ({keyword['score']:.4f}) "
            for keyword in keyword_items
        ]

        return (
            f"text: {self.text}, \n"
            f"id: {self.id}, \n"
            f"source: {self.source}, \n"
            f"keywords: {formatted_keywords}, \n"
            f"ner: {formatted_ner}, \n"
            f"vector: {self.vector}" # Enable if you want to print ALOT of numbers
        )

    