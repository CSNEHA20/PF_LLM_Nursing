import os
from dotenv import load_dotenv
from pathlib import Path

# Determine backend root directory (two levels up from this file: config/ → backend/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Explicitly load the .env file from the backend folder so it works
# regardless of where uvicorn / the terminal is launched from.
load_dotenv(BASE_DIR / ".env")

class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")

settings = Settings()

# Debug check to confirm API key is loaded
if not settings.GEMINI_API_KEY:
    print("DEBUG ERROR: GEMINI_API_KEY is missing from environment variables.")
else:
    print("DEBUG SUCCESS: GEMINI_API_KEY loaded successfully.")
