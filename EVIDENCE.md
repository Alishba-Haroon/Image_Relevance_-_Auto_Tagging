# Evidence

Use this file to paste real command output as the project is run.

## Requirement 1 — Structured vision output

Test:
```text
POST /jobs/process-images
```

Expected proof:
- metadata contains subject, category, attributes, caption, confidence
- invalid model output is rejected

## Requirement 2 — Low-confidence handling

Expected proof:
```text
status = flagged
```

## Requirement 3 — Batch job + retries

Expected proof:
```text
job completed with processed_count and failed_count
```

## Requirement 4 — Semantic matching

Expected proof:
```text
red fox post -> red fox image ranked first
```

## Requirement 5 — Mismatch guard

Expected proof:
```text
wolf candidate for fox post -> REJECTED
```

## Requirement 6 — No confident match

Expected proof:
```text
NO_CONFIDENT_MATCH
```

## Requirement 7 — Top-1 precision

Run:
```bash
python scripts/evaluate.py
```

Paste the actual output here.

## Requirement 8 — Cost tracking

Run:
```text
GET /costs
```

Paste the actual response here.

## Requirement 9 — Review API

Run:
```text
POST /reviews
```

Paste the actual response here.
