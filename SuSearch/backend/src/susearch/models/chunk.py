class Chunk:
    def __init__(self, text: str, source: str, keywords: list[str], keynames, vector):
        self.text = text
        self.source = source
        self.keywords = keywords
        self.keynames = keynames
        self.vector = vector

    def __str__(self):
        return f"text: {self.text}, source: {self.source}, keywords: {self.keywords}, ner: {self.keynames} vector: {self.vector}"

    