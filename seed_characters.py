
import asyncio
import json

from pathlib import Path
from sqlalchemy import select

from database import SessionLocal, engine
from models import Character
from schemas import CharacterCreate

DATA_FILE = Path(__file__).parent / "data" / "characters.json"

async def seed_characters():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        characters_data = json.load(f)
        
    async with SessionLocal() as session:
        created = 0
        updated = 0
        
        for item in characters_data:
            character_data = CharacterCreate.model_validate(item)
            statement = select(Character).where(Character.name == character_data.name)
            
            result = await session.execute(statement)
            character = result.scalar_one_or_none()
            
            if character is None:
                character = Character(**character_data.model_dump(), type="character")
                session.add(character)
                created += 1
                
            else:
                for key, value in character_data.model_dump().items():
                    setattr(character, key, value)
                updated += 1
                
        await session.commit()
        
        print(f"Created: {created} characters.")
        print(f"Updated: {updated} characters.")
        
async def main():
    try:
        await seed_characters()
    finally:
        await engine.dispose()
        
if __name__ == "__main__":
    asyncio.run(main())