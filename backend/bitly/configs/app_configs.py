
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(".vscode/.env")

# Database configurations
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/bitly_db")

# Redis configurations
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Sentry configurations
SENTRY_DSN = os.getenv("SENTRY_DSN")
SENTRY_TRANSACTION_STYLE = os.getenv("SENTRY_TRANSACTION_STYLE", "url")

