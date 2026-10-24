import asyncio
import os

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


async def main():
    load_dotenv(".env", override=True)

    engine = create_async_engine(os.environ["DATABASE_URL"])

    try:
        async with engine.begin() as connection:
            result = await connection.execute(
                text(
                    "DELETE FROM alembic_version "
                    "WHERE version_num = :revision "
                    "AND EXISTS ("
                    "SELECT 1 FROM alembic_version "
                    "WHERE version_num = :head"
                    ")"
                ),
                {
                    "revision": "d17d27904411",
                    "head": "f573f7330247",
                },
            )
            print(f"Deleted obsolete revision rows: {result.rowcount}")

    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())