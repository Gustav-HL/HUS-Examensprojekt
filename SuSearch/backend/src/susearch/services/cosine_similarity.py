import torch
import torch.nn.functional as F
from models.chunk import Chunk

class cosineSimilarityCalculator:

    def calculateChunks(self, query_vector, chunks: list[Chunk]) -> dict[str, float]:
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
        scores = torch.mv(chunks, query_vector)

        chunks = [c for c in chunks if c.vector is not None and len(c.vector) > 0]
        if not chunks:
            return {}

        matrix = torch.as_tensor([c.vector for c in chunks], dtype=torch.float32)
        query = torch.as_tensor(query_vector, dtype=torch.float32)

        scores = ((torch.mv(matrix, query) + 1) / 2).clamp(0, 1).tolist()

        ranked = sorted(
            zip((c.id for c in chunks), scores),
            key=lambda pair: pair[1],
            reverse=True,
        )

        return dict(ranked)

    def calculateStrings(self, query_vector, chunk_vectors) -> dict[int, float]:
        valid = [
            (i, vec)
            for i, vec in enumerate(chunk_vectors)
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