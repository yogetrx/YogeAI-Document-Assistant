# Data dictionary

## Chunk record
- `document_name` (string): original uploaded filename; production should use a generated document ID too.
- `page` (integer): 1-based original PDF page number.
- `chunk_id` (string): page-local identifier such as `p2-c1`.
- `text` (string): extracted chunk text.
- `score` (float, response only): similarity score from normalized vector inner-product search; not a probability.

## Ask request
- `question` (string, required): natural-language question, 1-2000 characters.
- `top_k` (integer, optional): number of passages to retrieve, 1-8.

## Ask response
- `answer` (string): generated answer.
- `sources` (array): retrieved chunks with document name, page, chunk ID, text, and score.
- `retrieval_count` (integer): number of source chunks returned.

## Evaluation record
- `id`: stable test case identifier.
- `document`: intended source document.
- `question`: question to ask.
- `expected_evidence`: key fact or absence-of-evidence expectation.
- `answerable`: whether the sample data contains sufficient evidence to answer.
