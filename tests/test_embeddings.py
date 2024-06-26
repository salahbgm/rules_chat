# From pytest, test the embeddings function `get_embedding_function`:
import pytest
from scripts.embedding import get_embedding_function


def test_get_embedding_function():
    result = get_embedding_function()
    assert result is not None, "Embedding function is None"
