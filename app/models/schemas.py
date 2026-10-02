from pydantic import BaseModel, Field
from typing import List, Literal

class VisionMetadata(BaseModel):
    subject: str = Field(min_length=1)
    category: str = Field(min_length=1)
    attributes: List[str] = Field(default_factory=list)
    caption: str = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)

class ReviewCreate(BaseModel):
    post_id: int
    image_id: int
    decision: Literal["approve", "reject"]
    reason: str = ""

class MatchResult(BaseModel):
    image_id: int
    filename: str
    similarity: float
    status: str
    explanation: str
