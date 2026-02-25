from pydantic import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str
    JWT_SECRET: str = "dev-secret"
    ENV: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()
