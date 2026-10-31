
import os
from pathlib import Path

import pytest_asyncio
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_TEST_PATH = PROJECT_ROOT / ".env.test"

if not ENV_TEST_PATH.is_file():
    raise FileNotFoundError(
        f".env.test not found: {ENV_TEST_PATH}"
    )

load_dotenv(ENV_TEST_PATH, override=True)

test_database_url = os.getenv("DATABASE_URL")

if not test_database_url:
    raise ValueError("DATABASE_URL is missing in .env.test")

if "onkapi_test" not in test_database_url:
    raise ValueError(
        "Tests must use the onkapi_test database. "
        f"Current URL: {test_database_url.split('@')[-1]}"
    )

import database
import deps
import main
from models import Base


@pytest_asyncio.fixture
async def client(monkeypatch):
    test_engine = create_async_engine(test_database_url)

    test_session_local = async_sessionmaker(
        test_engine,
        expire_on_commit=False,
    )

    monkeypatch.setattr(
        database, "SessionLocal", test_session_local
    )
    monkeypatch.setattr(
        main, "SessionLocal", test_session_local
    )
    monkeypatch.setattr(
        deps, "SessionLocal", test_session_local
    )

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    transport = ASGITransport(app=main.app)

    try:
        async with AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as test_client:
            yield test_client
    finally:
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

        await test_engine.dispose()


@pytest_asyncio.fixture
async def auth_headers(client):
    await client.post(
        "/auth/register",
        json={
            "username": "TestUser",
            "email": "testuser@example.com",
            "password": "testpassword123",
        },
    )

    response = await client.post(
        "/auth/login",
        data={
            "username": "TestUser",
            "password": "testpassword123",
        },
    )

    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}
