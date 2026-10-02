import json
from pathlib import Path
from app.models.schemas import VisionMetadata
from app.core.config import settings

DEMO_LABELS = {
    "fox": ("red fox", "animal", ["orange fur", "wild", "forest"]),
    "wolf": ("gray wolf", "animal", ["gray fur", "wild", "forest"]),
    "dog": ("dog", "animal", ["fur", "domestic", "pet"]),
    "bear": ("brown bear", "animal", ["brown fur", "wild", "forest"]),
}

def classify_demo(filename: str) -> VisionMetadata:
    name = filename.lower()
    for key, (subject, category, attrs) in DEMO_LABELS.items():
        if key in name:
            return VisionMetadata(
                subject=subject,
                category=category,
                attributes=attrs,
                caption=f"A {subject} in a natural setting",
                confidence=0.94,
            )
    return VisionMetadata(
        subject="unknown animal",
        category="animal",
        attributes=[],
        caption="An animal image",
        confidence=0.50,
    )

def classify_image(path: str) -> VisionMetadata:
    if settings.demo_mode:
        return classify_demo(Path(path).name)
    raise RuntimeError(
        "Real Gemini vision integration is intentionally isolated here. "
        "Configure the Gemini SDK/API call in app/services/vision.py before production use."
    )

def validate_metadata(payload: dict) -> VisionMetadata:
    return VisionMetadata.model_validate(payload)
