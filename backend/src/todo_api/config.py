import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: str = os.environ["DATABASE_URL"]
BETTER_AUTH_SECRET: str = os.environ["BETTER_AUTH_SECRET"]
CORS_ORIGINS: list[str] = [
    origin.strip()
    for origin in os.environ.get("CORS_ORIGINS", "http://localhost:3000").split(",")
]
OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")
