import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.db import SessionLocal
from app.models.entities import Post, ImageRecord
from app.services.embeddings import cosine_similarity
from app.services.guard import check_guard
import ast

db = SessionLocal()
posts = db.query(Post).all()
images = db.query(ImageRecord).all()

correct = 0
for post in posts:
    pv = ast.literal_eval(post.embedding)
    ranked = []
    for image in images:
        sim = cosine_similarity(pv, ast.literal_eval(image.embedding))
        status, _ = check_guard(post, image, sim)
        if status == "ACCEPTED":
            ranked.append((sim, image))
    ranked.sort(key=lambda x: x[0], reverse=True)
    if ranked and post.expected_subject.lower() in ranked[0][1].subject.lower():
        correct += 1

precision = correct / len(posts) if posts else 0
print(f"Top-1 precision: {precision:.4f}")
print(f"Correct: {correct}/{len(posts)}")
db.close()
