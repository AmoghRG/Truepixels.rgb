"""Configuration settings for Module M1 (Image & Access Management)."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Security & JWT
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev_secret_key_truepixels_rgb_84739274927394829374829374928374")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
SESSION_EXPIRE_HOURS = int(os.getenv("SESSION_EXPIRE_HOURS", "8"))

# Storage Configuration
STORAGE_DIR = Path(os.getenv("STORAGE_DIR", str(BASE_DIR / "storage")))
UPLOADS_DIR = STORAGE_DIR / "uploads"
TENSORS_DIR = STORAGE_DIR / "tensors"

UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
TENSORS_DIR.mkdir(parents=True, exist_ok=True)

# Validation Bounds
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "10"))
MAX_UPLOAD_SIZE_BYTES = MAX_UPLOAD_SIZE_MB * 1024 * 1024
MIN_IMAGE_DIMENSION = int(os.getenv("MIN_IMAGE_DIMENSION", "64"))
MAX_IMAGE_PIXELS = int(os.getenv("MAX_IMAGE_PIXELS", "25000000"))  # Guard against decompression bombs (5000x5000)

# Email / 2FA Configuration
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "smtp")
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_USER = os.getenv("SMTP_USER", "i.practice.java@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM = os.getenv("SMTP_FROM", "i.practice.java@gmail.com")
SMTP_USE_SSL = os.getenv("SMTP_USE_SSL", "True").lower() in ("true", "1", "yes")
OTP_EXPIRE_MINUTES = int(os.getenv("OTP_EXPIRE_MINUTES", "5"))
REQUIRE_2FA = os.getenv("REQUIRE_2FA", "False").lower() in ("true", "1", "yes")
