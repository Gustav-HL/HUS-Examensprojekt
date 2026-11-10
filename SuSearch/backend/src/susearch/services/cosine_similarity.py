import torch

class cosineSimilarityCalculator:

    def calculate(self, query_vector, document_vectors):
        scores = torch.mv(document_vectors, query_vector)

        return (scores + 1) / 2