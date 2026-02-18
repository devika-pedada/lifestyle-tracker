import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Lifestyle Tracker")
    ENV: str = os.getenv("ENV", "dev")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "database_url")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "secret_key")


settings = Settings()
