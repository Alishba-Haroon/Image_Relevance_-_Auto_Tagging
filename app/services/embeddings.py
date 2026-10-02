import hashlib
import numpy as np

def deterministic_embedding(text: str, dims: int = 128) -> list[float]:
    # Stable local demo embedding. This is intentionally simple and deterministic.
    seed = int(hashlib.sha256(text.lower().encode()).hexdigest()[:16], 16)
    rng = np.random.default_rng(seed)
    vector = rng.normal(size=dims).astype(float)
    vector /= np.linalg.norm(vector) or 1.0
    return vector.tolist()

def cosine_similarity(a: list[float], b: list[float]) -> float:
    va, vb = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    denom = np.linalg.norm(va) * np.linalg.norm(vb)
    return float(np.dot(va, vb) / denom) if denom else 0.0
