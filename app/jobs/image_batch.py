from pathlib import Path
from sqlalchemy.orm import Session
from app.models.entities import ImageRecord, JobLog
from app.services.vision import classify_image
from app.services.embeddings import deterministic_embedding
from app.services.costs import record_cost
from app.core.config import settings

def process_image_batch(db: Session, image_dir: str) -> dict:
    paths = [p for p in Path(image_dir).rglob("*") if p.is_file()]
    processed = 0
    failed = 0

    for path in paths:
        attempts = 0
        last_error = ""
        while attempts < settings.max_retries:
            attempts += 1
            try:
                meta = classify_image(str(path))
                embedding = deterministic_embedding(meta.caption + " " + meta.subject)
                row = ImageRecord(
                    filename=str(path.relative_to(image_dir)),
                    subject=meta.subject,
                    category=meta.category,
                    attributes=str(meta.attributes),
                    caption=meta.caption,
                    confidence=meta.confidence,
                    status="accepted" if meta.confidence >= settings.confidence_threshold else "flagged",
                    embedding=str(embedding),
                )
                db.add(row)
                db.commit()
                record_cost(db, "vision+embedding", str(path), 0.0)
                db.add(JobLog(operation="image_batch", item_id=str(path), attempts=attempts, status="success"))
                db.commit()
                processed += 1
                break
            except Exception as exc:
                last_error = str(exc)
        else:
            failed += 1
            db.add(JobLog(operation="image_batch", item_id=str(path), attempts=attempts,
                          status="failed", error=last_error))
            db.commit()

    return {"processed": processed, "failed": failed, "total": len(paths)}
