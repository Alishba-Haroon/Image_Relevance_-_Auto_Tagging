from types import SimpleNamespace
from app.services.guard import check_guard

def test_guard_rejects_subject_mismatch():
    post = SimpleNamespace(expected_subject="red fox")
    image = SimpleNamespace(subject="gray wolf", confidence=0.95)
    status, reason = check_guard(post, image, 0.99)
    assert status == "REJECTED"
    assert "mismatch" in reason.lower()

def test_guard_accepts_good_match():
    post = SimpleNamespace(expected_subject="red fox")
    image = SimpleNamespace(subject="red fox", confidence=0.95)
    status, reason = check_guard(post, image, 0.90)
    assert status == "ACCEPTED"
