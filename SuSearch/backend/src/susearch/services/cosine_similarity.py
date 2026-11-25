import torch
import torch.nn.functional as F
from models.chunk import Chunk

class cosineSimilarityCalculator:

    def calculateChunks(self, query_vector, chunks: list[Chunk]) -> dict[str, dict]:
        """Calculates the cosine similarity between the query vector and the 
        vectors of a list of chunks. The value is then rescaled to a range between
        0 and 1.
        
        Args: 
            query_vector: The vector of the query.
            chunks: List of Chunk objects.
        
        Returns:
            A dictionary with the cosine similarity score and the id of the chunks.
            It is sorted with the highest cosine similarity score first.
        """
        chunks = [c for c in chunks if c.vector is not None and len(c.vector) > 0]
        if not chunks:
            return {}

        matrix = torch.as_tensor([c.vector for c in chunks], dtype=torch.float32)
        query = torch.as_tensor(query_vector, dtype=torch.float32)
        if query.dim() == 1:
            query = query.unsqueeze(0) 

        sims = (matrix @ query.T).max(dim=1).values
        scores = ((sims + 1) / 2).clamp(0, 1).tolist()

        ranked = sorted(
            zip(chunks, scores),
            key=lambda pair: pair[1],
            reverse=True,
        )

        return {c.id: {"doc_id": c.doc_id, "score": score} for c, score in ranked}

    def calculateStrings(self, query_vector, chunk_vectors) -> dict[str, float]:
        valid = [
            (i, vec)
            for i, vec in chunk_vectors.items()
            if vec is not None and len(vec) > 0
        ]
        if not valid:
            return {}

        ids, vectors = zip(*valid)

        matrix = torch.stack([torch.as_tensor(v, dtype=torch.float32).reshape(-1) for v in vectors])
        query = torch.as_tensor(query_vector, dtype=torch.float32).reshape(-1)  

        matrix = F.normalize(matrix, p=2, dim=1)
        query = F.normalize(query, p=2, dim=0)

        scores = torch.mv(matrix, query).tolist()

        ranked = sorted(zip(ids, scores), key=lambda pair: pair[1], reverse=True)
        return dict(ranked)