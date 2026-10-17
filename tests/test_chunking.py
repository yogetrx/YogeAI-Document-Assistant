import pytest
from src.yogeai_api.chunking import split_text

def test_empty_text():
    assert split_text("") == []

def test_short_text():
    assert split_text("hello world") == ["hello world"]

def test_long_text_splits():
    chunks = split_text("word " * 500, chunk_size=100, overlap=20)
    assert len(chunks) > 1
    assert all(len(c) <= 100 for c in chunks)

def test_invalid_overlap_raises():
    with pytest.raises(ValueError):
        split_text("some text", chunk_size=10, overlap=10)
