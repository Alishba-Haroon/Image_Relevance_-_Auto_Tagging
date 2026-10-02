import ast
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.config import settings
from app.models.entities import ImageRecord, Post, Review, CostLog
from app.models.schemas import ReviewCreate
from app.services.embeddings import deterministic_embedding, cosine_similarity
from app.services.guard import check_guard
from app.jobs.image_batch import process_image_batch

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok", "demo_mode": settings.demo_mode}

@router.get("/images")
def images(db: Session = Depends(get_db)):
    rows = db.query(ImageRecord).all()
    return [{"id": r.id, "filename": r.filename, "subject": r.subject,
             "category": r.category, "confidence": r.confidence, "status": r.status} for r in rows]

@router.get("/posts")
def posts(db: Session = Depends(get_db)):
    return [{"id": p.id, "title": p.title, "expected_subject": p.expected_subject,
             "expected_category": p.expected_category} for p in db.query(Post).all()]

@router.post("/jobs/process-images")
def process_images(db: Session = Depends(get_db)):
    return process_image_batch(db, "data/images")

@router.get("/posts/{post_id}/images")
def match_images(post_id: int, db: Session = Depends(get_db)):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(404, "Post not found")

    post_vec = ast.literal_eval(post.embedding)
    results = []
    for image in db.query(ImageRecord).all():
        image_vec = ast.literal_eval(image.embedding)
        sim = cosine_similarity(post_vec, image_vec)
        status, explanation = check_guard(post, image, sim)
        results.append({
            "image_id": image.id,
            "filename": image.filename,
            "similarity": round(sim, 4),
            "status": status,
            "explanation": explanation,
        })

    results.sort(key=lambda x: x["similarity"], reverse=True)
    accepted = [x for x in results if x["status"] == "ACCEPTED"]
    if not accepted:
        return {"status": "NO_CONFIDENT_MATCH", "results": results,
                "reason": "No candidate passed the mismatch guard."}
    return {"status": "MATCH_FOUND", "results": results}

@router.post("/reviews")
def create_review(payload: ReviewCreate, db: Session = Depends(get_db)):
    if not db.get(Post, payload.post_id) or not db.get(ImageRecord, payload.image_id):
        raise HTTPException(404, "Post or image not found")
    row = Review(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"id": row.id, **payload.model_dump()}

@router.get("/reviews")
def reviews(db: Session = Depends(get_db)):
    return [r.__dict__ for r in db.query(Review).all()]

@router.get("/costs")
def costs(db: Session = Depends(get_db)):
    rows = db.query(CostLog).all()
    return {
        "total_estimated_cost_usd": round(sum(r.estimated_cost_usd for r in rows), 6),
        "calls": [{"operation": r.operation, "item_id": r.item_id,
                   "estimated_cost_usd": r.estimated_cost_usd} for r in rows],
    }

@router.get("/evaluation")
def evaluation(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    if not posts:
        return {"top1_precision": 0.0, "evaluated": 0}
    correct = 0
    for post in posts:
        post_vec = ast.literal_eval(post.embedding)
        candidates = []
        for image in db.query(ImageRecord).all():
            sim = cosine_similarity(post_vec, ast.literal_eval(image.embedding))
            status, _ = check_guard(post, image, sim)
            candidates.append((sim, status, image.subject))
        candidates.sort(reverse=True)
        accepted = [x for x in candidates if x[1] == "ACCEPTED"]
        if accepted and post.expected_subject.lower() in accepted[0][2].lower():
            correct += 1
    return {"top1_precision": round(correct / len(posts), 4), "correct": correct, "evaluated": len(posts)}
