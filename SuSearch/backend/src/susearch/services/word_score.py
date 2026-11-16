import re
import math

class wordScorer:
    def get_score(self, chunks, keyword):
        document = " ".join(chunks).lower()
        keyword = keyword.lower().strip()

        words = re.findall(r'\b\w+\b', document)

        if not words or not keyword:
            return 0.0

        pattern = r'\b' + re.escape(keyword) + r'\b'
        occurrences = len(re.findall(pattern, document))

        if occurrences == 0:
            return 0.0

        tf = occurrences / len(words)
        score = 1 - math.exp(-5 * tf)

        return round(score, 2)