import pytest
import torch
from SuSearch.backend.src.susearch.services.vector_extractor import Vectorizer

def test_vectorize_vector_shape():
    chunk = ["Denna metoden testar vektoriseringen i ett program skrivet i python."]
    vectorizer = Vectorizer()
    expected = 768
    actual = torch.as_tensor(vectorizer.vectorize(chunk))
    assert expected == actual.shape[-1]