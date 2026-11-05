import pytest

from tracemate.rag.vector_store import VectorStore


def test_valid_embeddings():
    VectorStore._validate_embeddings(
        [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]],
        expected_count=2,
    )


def test_wrong_embedding_count():
    with pytest.raises(ValueError):
        VectorStore._validate_embeddings(
            [[0.1, 0.2]],
            expected_count=2,
        )


def test_inconsistent_dimensions():
    with pytest.raises(ValueError):
        VectorStore._validate_embeddings(
            [[0.1, 0.2], [0.3, 0.4, 0.5]],
            expected_count=2,
        )


@pytest.mark.parametrize("invalid_value", [float("nan"), float("inf"), float("-inf")])
def test_non_finite_embedding_values(invalid_value):
    with pytest.raises(ValueError):
        VectorStore._validate_embeddings(
            [[0.1, invalid_value]],
            expected_count=1,
        )


def test_empty_embedding():
    with pytest.raises(ValueError):
        VectorStore._validate_embeddings(
            [[]],
            expected_count=1,
        )