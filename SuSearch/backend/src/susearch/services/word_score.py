import re
import math

class wordScorer:
    def get_score(self, chunks, keyword):
        document = " ".join(chunks)
        words = re.findall(r'\b\w+\b', document.lower())
        keyword = keyword.lower()

        if not words:
            return 0.0

        occurrences = words.count(keyword)

        if occurrences == 0:
            return 0.0

        tf = occurrences / len(words)

        score = 1 - math.exp(-5 * tf)

        return round(score, 2)