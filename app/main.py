from fastapi import FastAPI
from app.core.db import Base, engine
from app.api.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FlyRank AI Image Matching Engine", version="1.0.0")
app.include_router(router)
