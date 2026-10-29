import torch
import torch.nn.functional as F
from transformers import AutoModel, AutoTokenizer
from models.chunk import Chunk

class Vectorizer:
    def __init__(
        self,
        model_name: str = "KBLab/sentence-bert-swedish-cased",
        max_tokens: int = 384,  
        batch_size: int = 16,
        device: str | None = None,
    ):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(self.device).eval()
        self.max_tokens = max_tokens
        self.batch_size = batch_size

    # combines the vectors of each token to one vector with the average value, padding tokens are ignored.
    @staticmethod 
    def _mean_pooling(token_embeddings, attention_mask):
        mask = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return (token_embeddings * mask).sum(1) / mask.sum(1).clamp(min=1e-9)

    # counts the amount of chunks with more tokens than max_tokens
    def _warn_if_truncated(self, texts: list[str]) -> None:
        too_long = sum(
            len(self.tokenizer(t, add_special_tokens=True)["input_ids"]) > self.max_tokens
            for t in texts
        )
        if too_long:
            print(f"Warning: {too_long} av {len(texts)} chunks är längre än "
                  f"{self.max_tokens} tokens och klipps av.")

    @torch.no_grad()
    def vectorize(self, texts: list[Chunk]) -> torch.Tensor:
        if not texts:
            return torch.empty(0, self.model.config.hidden_size)

        self._warn_if_truncated(texts)

        order = sorted(range(len(texts)), key=lambda i: len(texts[i]))
        embeddings = [None] * len(texts)

        for start in range(0, len(order), self.batch_size):
            idx = order[start:start + self.batch_size]
            batch = self.tokenizer(
                [texts[i] for i in idx],
                padding=True,
                truncation=True,
                max_length=self.max_tokens,
                return_tensors="pt",
            ).to(self.device)

            output = self.model(**batch)
            emb = self._mean_pooling(output[0], batch["attention_mask"])
            emb = F.normalize(emb, p=2, dim=1).cpu()

            for i, e in zip(idx, emb):
                embeddings[i] = e

        return torch.stack(embeddings)

    def vectorize_chunks(self, chunks: list[str]) -> torch.Tensor:
        return self.vectorize([c for c in chunks])