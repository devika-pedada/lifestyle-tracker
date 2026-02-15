import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Lifestyle Tracker")
    ENV: str = os.getenv("ENV", "dev")


settings = Settings()
