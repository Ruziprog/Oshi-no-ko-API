from sqlalchemy import ForeignKey, String, select
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
import asyncio

DATABASE_URL = "sqlite+aiosqlite:///./oshi_no_ko.db"

engine = create_async_engine(
    DATABASE_URL, 
    echo=True
)

SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(100), nullable=False)


class Character(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    age: Mapped[int] = mapped_column()
    description: Mapped[str] = mapped_column(String(200))
    role: Mapped[str] = mapped_column(String(50))

    type: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "character"
    }

class Idol(Character):
    __tablename__ = "idols"

    id: Mapped[int] = mapped_column(
        ForeignKey("characters.id"), 
        primary_key=True
        )


    songs: Mapped[list["Song"]] = relationship(
        "Song", 
        back_populates="idol"
        )

    __mapper_args__ = {
        "polymorphic_identity": "idol"
        }

class Song(Base):
    __tablename__ = "songs"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    idol_id: Mapped[int] = mapped_column(
        ForeignKey("idols.id")
    )

    idol: Mapped["Idol"] = relationship(
        back_populates="songs"
    )



async def create_ai():
    async with SessionLocal() as session:
        ai = Idol(
            name="Ai Hoshino",
            age=16,
            description="A famous idol and the mother of Aqua and Ruby.",
            role="Idol",
        )

        song = Song(
            title="Idol Song 1",
            idol=ai
        )

        session.add(ai)
        session.add(song)
        await session.commit()

async def create_ruby():
    async with SessionLocal() as session:
        ruby = Idol(
            name="Ruby Hoshino",
            age=16,
            description="The daughter of Ai Hoshino and a talented idol in her own right.",
            role="Idol",
        )

        song1 = Song(title="STAR☆T☆RAIN", idol=ruby)
        song2 = Song(title="Sign wa B", idol=ruby)
        song3 = Song(title="B-revenge", idol=ruby)

        session.add(ruby)
        session.add_all([song1, song2, song3])
        await session.commit()

async def create_aqua():
    async with SessionLocal() as session:
        aqua = Character(
            name="Aqua Hoshino",
            age=16,
            description="The son of Ai Hoshino and a rising star in the acting world.",
            role="Actor"
        )

        session.add(aqua)
        await session.commit()

async def get_character():
    async with SessionLocal() as session:
        statement = select(Character)
        result = await session.execute(statement)
        characters = result.scalars().all()
        return characters

async def get_character_by_name(character_name: str):
    async with SessionLocal() as session:
        statement = select(Character).where(Character.name == character_name)
        result = await session.execute(statement)
        character = result.scalar_one_or_none()
        return character



async def get_character_by_role(character_role: str):
    async with SessionLocal() as session:
        statement = select(Character).where(Character.role == "Idol")
        result = await session.execute(statement)
        characters = result.scalars().all()
        return characters

async def get_all_sixteens():
    async with SessionLocal() as session:
        statement = select(Character).where(Character.age == 16)
        result = await session.execute(statement)
        characters = result.scalars().all()
        return characters

async def update_character_age(name: str, age: int):
    async with SessionLocal() as session:
        statement = select(Character).where(Character.name == name)
        result = await session.execute(statement)
        character = result.scalar_one_or_none()
        character.age = age
        await session.commit()

async def delete_character(name: str):
    async with SessionLocal() as session:
        statement = select(Character).where(Character.name == name)
        result = await session.execute(statement)
        character = result.scalar_one_or_none()
        await session.delete(character)
        await session.commit()


async def main():
    await create_ai()
    await create_ruby()
    await create_aqua()
    await delete_character("Ai Hoshino")
    await update_character_age("Ruby Hoshino", 19)
    await update_character_age("Aqua Hoshino", 18)
    characters = await get_character()
    for character in characters:
        print(character.name)

if __name__ == "__main__":
    asyncio.run(main())