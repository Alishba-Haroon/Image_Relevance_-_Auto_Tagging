# FlyRank Capstone — AI Image Understanding & Content Matching Engine

A production-style FastAPI service that understands a small image corpus, creates structured metadata, embeds image captions and blog posts, ranks semantically relevant images, and rejects unsafe/low-confidence matches through a mismatch guard.

## Architecture

```text
Images
  |
  v
Batch Vision Job
  |
  +--> Pydantic Schema Validation
  |
  +--> image_metadata
  |
  +--> Caption Embedding ----                              > Similarity Ranking -> Mismatch Guard -> Suggestion
Blog Posts -> Post Embedding-/
                                      |
                                      +--> Review API: approve/reject
```

## Core requirements covered

- Structured vision output with schema validation
- Low-confidence flagging
- Batch processing with retries
- Per-call cost tracking
- Semantic similarity ranking
- Mismatch guard with human-readable explanations
- "No confident match" behavior
- Review API
- Evaluation dataset and Top-1 precision
- Layered architecture
- Environment-based secrets
- Public-repo-ready documentation

The capstone brief requires 40+ images across 4+ categories and 10+ labeled evaluation posts. The included seed script creates the database records and local demo corpus structure; add licensed images to the category folders before running a real vision batch.

## Stack

- Python 3.11+
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite for zero-setup local development
- NumPy
- Gemini API optional for real vision/embeddings
- Deterministic local demo mode for offline testing

## Setup

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
python scripts/seed_demo.py
uvicorn app.main:app --reload
```

Open API docs at `http://127.0.0.1:8000/docs`.

## Demo mode

The project runs without an API key using `DEMO_MODE=true`. This mode provides deterministic metadata and embeddings so the complete matching/guard/evaluation workflow can be demonstrated safely.

For real Gemini processing, set `DEMO_MODE=false` and provide `GEMINI_API_KEY`.

## Main endpoints

- `GET /health`
- `GET /images`
- `GET /posts`
- `POST /jobs/process-images`
- `GET /posts/{post_id}/images`
- `POST /reviews`
- `GET /reviews`
- `GET /evaluation`
- `GET /costs`

Example:

```bash
curl http://127.0.0.1:8000/posts/1/images
```

## Evaluation

```bash
python scripts/evaluate.py
```

The script reports Top-1 precision over the labeled evaluation set.

## Mismatch guard

The guard combines:

1. semantic similarity
2. category/subject compatibility
3. confidence threshold

Example expected behavior:

```text
Post: The behavior of red foxes
Candidate: Gray wolf in the forest
Result: REJECTED
Reason: Animal category mismatch: expected fox, detected wolf
```

If no candidate clears the configured threshold:

```text
NO_CONFIDENT_MATCH
Reason: similarity below threshold and/or subject mismatch
```

## Required submission files

- `README.md`
- `capstone.yaml`
- `EVIDENCE.md`
- `BUILDLOG.md`
- `.env.example`

## Limitations

The demo mode uses deterministic local metadata/embeddings rather than a real vision model. For a production submission, populate the corpus with licensed images and run the Gemini vision/embedding path. Thresholds should be tuned against the final labeled evaluation set rather than assumed.
# Image_Relevance_-_Auto_Tagging
