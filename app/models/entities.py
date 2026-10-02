from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean

from app.core.db import Base

class ImageRecord(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    category = Column(String, nullable=False)
    attributes = Column(Text, default="[]")
    caption = Column(Text, nullable=False)
    confidence = Column(Float, nullable=False)
    status = Column(String, default="accepted")
    embedding = Column(Text, default="[]")
    created_at = Column(DateTime, default=datetime.utcnow)

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    expected_subject = Column(String, nullable=False)
    expected_category = Column(String, nullable=False)
    embedding = Column(Text, default="[]")

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, nullable=False)
    image_id = Column(Integer, nullable=False)
    decision = Column(String, nullable=False)
    reason = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

class CostLog(Base):
    __tablename__ = "cost_logs"
    id = Column(Integer, primary_key=True)
    operation = Column(String, nullable=False)
    item_id = Column(String, nullable=False)
    estimated_cost_usd = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

class JobLog(Base):
    __tablename__ = "job_logs"
    id = Column(Integer, primary_key=True)
    operation = Column(String, nullable=False)
    item_id = Column(String, nullable=False)
    attempts = Column(Integer, default=1)
    status = Column(String, nullable=False)
    error = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
