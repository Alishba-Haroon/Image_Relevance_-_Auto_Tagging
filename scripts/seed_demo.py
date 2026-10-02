import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.db import Base, engine, SessionLocal
from app.models.entities import ImageRecord, Post
from app.services.embeddings import deterministic_embedding

Base.metadata.create_all(bind=engine)
db = SessionLocal()

if db.query(ImageRecord).count() == 0:
    categories = {
        "fox": ("red fox", "animal", ["orange fur", "wild", "forest"]),
        "wolf": ("gray wolf", "animal", ["gray fur", "wild", "forest"]),
        "dog": ("dog", "animal", ["fur", "domestic", "pet"]),
        "bear": ("brown bear", "animal", ["brown fur", "wild", "forest"]),
    }
    for category, (subject, _, _) in categories.items():
        folder = Path("data/images") / category
        folder.mkdir(parents=True, exist_ok=True)
        for i in range(1, 11):
            (folder / f"{category}_{i}.jpg").touch()
            caption = f"A {subject} in a natural setting"
            db.add(ImageRecord(
                filename=f"{category}/{category}_{i}.jpg",
                subject=subject,
                category="animal",
                attributes="[]",
                caption=caption,
                confidence=0.94,
                status="accepted",
                embedding=str(deterministic_embedding(caption + " " + subject))
            ))

posts = [
    ("Red Fox Behavior", "Understanding the behavior and habitat of red foxes.", "red fox"),
    ("Fox Habitat", "Where red foxes live and how they survive in forests.", "red fox"),
    ("Fox Species", "A guide to the red fox as a wild fox species.", "red fox"),
    ("Wolf Behavior", "How gray wolves behave and hunt in the wild.", "gray wolf"),
    ("Wolf Habitat", "The forest habitat and life of gray wolves.", "gray wolf"),
    ("Domestic Dogs", "An overview of dogs and their relationship with people.", "dog"),
    ("Dog Companions", "Why dogs are common household pets.", "dog"),
    ("Brown Bear Habitat", "Where brown bears live and find food.", "brown bear"),
    ("Bear Behavior", "The behavior of brown bears in the wild.", "brown bear"),
    ("Wild Bear Species", "Understanding brown bears as a wild species.", "brown bear"),
]

if db.query(Post).count() == 0:
    for title, content, subject in posts:
        db.add(Post(
            title=title,
            content=content,
            expected_subject=subject,
            expected_category="animal",
            embedding=str(deterministic_embedding(content + " " + subject))
        ))

db.commit()
db.close()
print("Demo database seeded: 40 images + 10 labeled posts.")
