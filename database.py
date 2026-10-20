from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

# SQL echo can log query parameters, including personal data.
# Enable it explicitly only when debugging locally.
SQL_ECHO = os.getenv("SQL_ECHO", "false").strip().lower() in {
    "1",
    "true",
    "yes",
}

engine = create_async_engine(
    DATABASE_URL,
    echo=SQL_ECHO,
)


SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)
