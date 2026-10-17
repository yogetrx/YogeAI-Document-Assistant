# Sample data

The `.md` files in `sample_docs/` are synthetic test documents. To generate PDFs for upload testing, install `reportlab` and run:

```powershell
pip install reportlab
python data/generate_sample_pdfs.py
```

Evaluation questions live in `evaluation/questions.json`. The `expected_page_note` field is a note for the evaluator, not a guaranteed PDF page number. Confirm actual citations against the generated PDF.
