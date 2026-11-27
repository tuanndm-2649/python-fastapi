import os
from pathlib import Path

from dotenv import load_dotenv

from demo_fastapi.constants.message import (
    DATABASE_URL_NOT_FOUND,
    SECRET_KEY_NOT_FOUND,
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(PROJECT_ROOT / ".env")

SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
SMTP_PORT = int(os.getenv("SMTP_PORT", "1025"))
SMTP_FROM = os.getenv("SMTP_FROM", "no-reply@taskhub.local")
REDIS_URL = os.getenv("REDIS_URL")

if not DATABASE_URL:
    raise RuntimeError(DATABASE_URL_NOT_FOUND)

if not SECRET_KEY:
    raise RuntimeError(SECRET_KEY_NOT_FOUND)
