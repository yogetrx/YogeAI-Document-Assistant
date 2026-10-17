# Test plan

## Functional
1. Upload valid text PDF; expect indexed status and positive chunk count.
2. Upload non-PDF; expect HTTP 400.
3. Upload PDF with no selectable text; expect HTTP 422 and OCR guidance.
4. Ask a question with indexed data; expect answer and source records.
5. Ask an unanswerable question; expect explicit uncertainty rather than invented facts.

## Retrieval quality
For each row in `data/evaluation/questions.json`, record:
- whether the expected evidence appears in top-k retrieved chunks,
- whether the answer is supported by the retrieved evidence,
- whether citation document/page is correct,
- whether unanswerable questions are refused appropriately.

## Security
- Verify `.env` is not committed.
- Test oversized file rejection.
- Treat document text as untrusted.
- Before deployment, add authentication, per-document authorization, rate limiting, and malware scanning.

## Suggested metrics
- Recall@k for evidence retrieval.
- Citation precision: cited sources support the corresponding claims.
- Grounded answer rate.
- Unanswerable-question refusal accuracy.
- Latency and model token/cost metrics where available.
