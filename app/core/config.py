from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "FlyRank Image Relevance Engine"
    database_url: str = "sqlite:///./flyrank.db"
    demo_mode: bool = True
    gemini_api_key: str = ""
    vision_model: str = "gemini-2.5-flash"
    embedding_model: str = "gemini-embedding-001"
    similarity_threshold: float = 0.55
    confidence_threshold: float = 0.70
    max_retries: int = 3
    cost_budget_usd: float = 0.0

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
