
import json
from pathlib import Path

from sqlalchemy import select

from database import SessionLocal
from models import Character


BASE_DIR = Path(__file__).resolve().parent
PROFILES_FILE = BASE_DIR / "data" / "character_profiles.json"


async def seed_profiles():
    with PROFILES_FILE.open("r", encoding="utf-8") as file:
        profiles = json.load(file)

    async with SessionLocal() as session:
        for profile_data in profiles:
            name = profile_data["name"]

            statement = select(Character).where(
                Character.name == name
            )

            result = await session.execute(statement)
            character = result.scalar_one_or_none()

            if character is None:
                print(f"Character not found: {name}")
                continue

            character.profile = {
                key: value
                for key, value in profile_data.items()
                if key != "name"
            }

            print(f"Profile updated: {name}")

        await session.commit()


if __name__ == "__main__":
    import asyncio

    asyncio.run(seed_profiles())
