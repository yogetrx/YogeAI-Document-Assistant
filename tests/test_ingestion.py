from src.yogeai_api.ingestion import make_records

def test_make_records_preserves_document_and_page_metadata():
    records = make_records(
        "policy.pdf",
        [{"page": 3, "text": "Customers may request a refund within 14 days."}],
    )
    assert len(records) == 1
    assert records[0]["document_name"] == "policy.pdf"
    assert records[0]["page"] == 3
    assert records[0]["chunk_id"] == "p3-c1"
