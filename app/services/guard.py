from app.core.config import settings

def check_guard(post, image, similarity: float) -> tuple[str, str]:
    if image.confidence < settings.confidence_threshold:
        return "REJECTED", f"Low vision confidence: {image.confidence:.2f}"

    if post.expected_subject.lower() not in image.subject.lower():
        return "REJECTED", (
            f"Subject mismatch: expected {post.expected_subject}, detected {image.subject}"
        )

    if similarity < settings.similarity_threshold:
        return "REJECTED", (
            f"Similarity {similarity:.3f} is below threshold "
            f"{settings.similarity_threshold:.3f}"
        )

    return "ACCEPTED", "Subject, confidence, and semantic similarity passed the guard."
