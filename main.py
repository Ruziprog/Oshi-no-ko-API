from uuid import UUID
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import select
from deps import get_current_user
from sqlalchemy.orm import selectinload

from fastapi.security import OAuth2PasswordRequestForm
from database import SessionLocal
from security import (
    hash_password,
    verify_password,
    create_access_token,
)
from models import User, Character, Song, Idol
from schemas import (
    UserCreate,
    CharacterCreate,
    CharacterResponse,
    SongCreate,
    SongResponse,
)


app = FastAPI(title="Oshi no Ko API", description="API for Oshi no Ko", version="1.0.0")


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Oshi no Ko API!"}

@app.post("/auth/register")
async def register(user: UserCreate):
    hashed_password = hash_password(user.password)

    async with SessionLocal() as session:
        new_user = User(
            username=user.username,
            email=user.email,
            password_hash=hashed_password
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        }

@app.post("/auth/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    async with SessionLocal() as session:
        statement = select(User).where(
            User.username == form_data.username
        )

        result = await session.execute(statement)
        db_user = result.scalar_one_or_none()

        if db_user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )

        if not verify_password(
            form_data.password,
            db_user.password_hash
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )

        access_token = create_access_token(
            db_user.username
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }


@app.get("/auth/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }


@app.get("/characters", response_model=list[CharacterResponse])
async def get_characters():
    async with SessionLocal() as session:
        statement = select(Character)
        result = await session.execute(statement)
        characters = result.scalars().all()
        return characters
    
    
@app.get(
    "/characters/{character_id}",
    response_model=CharacterResponse
)
async def get_character(character_id: UUID):
    async with SessionLocal() as session:
        statement = select(Character).where(
            Character.id == character_id
        )

        result = await session.execute(statement)

        character = result.scalar_one_or_none()

        if character is None:
            raise HTTPException(
                status_code=404,
                detail="Character not found"
            )

        return character
    
    
@app.post(
    "/characters",
    response_model=CharacterResponse,
    status_code=201
)
async def create_character(character: CharacterCreate, current_user: User = Depends(get_current_user)):
    async with SessionLocal() as session:
        new_character = Character(
            name=character.name,
            age=character.age,
            description=character.description,
            role=character.role,
            type="character"
        )

        session.add(new_character)

        await session.commit()
        await session.refresh(new_character)

        return new_character
    
    
@app.put(
    "/characters/{character_id}",
    response_model=CharacterResponse
)
async def update_character(
    character_id: UUID,
    character_data: CharacterCreate,
    current_user: User = Depends(get_current_user)):
    async with SessionLocal() as session:
        statement = select(Character).where(
            Character.id == character_id
        )

        result = await session.execute(statement)

        character = result.scalar_one_or_none()

        if character is None:
            raise HTTPException(
                status_code=404,
                detail="Character not found"
            )

        character.name = character_data.name
        character.age = character_data.age
        character.description = character_data.description
        character.role = character_data.role

        await session.commit()
        await session.refresh(character)

        return character
    
    
@app.delete("/characters/{character_id}")
async def delete_character(character_id: UUID, current_user: User = Depends(get_current_user)):
    async with SessionLocal() as session:
        statement = select(Character).where(
            Character.id == character_id
        )

        result = await session.execute(statement)

        character = result.scalar_one_or_none()

        if character is None:
            raise HTTPException(
                status_code=404,
                detail="Character not found"
            )

        await session.delete(character)
        await session.commit()

        return {
            "message": "Character deleted"
        }
        
@app.post(
    "/songs",
    response_model=SongResponse,
    status_code=201
)
async def create_song(
    song: SongCreate,
    current_user: User = Depends(get_current_user)
):
    async with SessionLocal() as session:

        statement = select(Idol).where(
            Idol.id.in_(song.idol_ids)
        )

        result = await session.execute(statement)
        idols = result.scalars().all()

        if len(idols) != len(set(song.idol_ids)):
            raise HTTPException(
                status_code=404,
                detail="One or more idols not found"
            )

        new_song = Song(
            title=song.title,
            idols=idols
        )

        session.add(new_song)

        await session.commit()
        await session.refresh(new_song)

        return {
            "id": new_song.id,
            "title": new_song.title,
            "idol_ids": [idol.id for idol in idols],
            "idol_names": [idol.name for idol in idols]
        }
    
    
@app.get(
    "/songs",
    response_model=list[SongResponse]
)
async def get_songs():
    async with SessionLocal() as session:

        statement = select(Song).options(
            selectinload(Song.idols)
        )

        result = await session.execute(statement)
        songs = result.scalars().all()

        return [
            {
                "id": song.id,
                "title": song.title,
                "idol_ids": [
                    idol.id for idol in song.idols
                ],
                "idol_names": [
                    idol.name for idol in song.idols
                ]
            }
            for song in songs
        ]
    
    
@app.get(
    "/songs/{song_id}",
    response_model=SongResponse
)
async def get_song(song_id: UUID):
    async with SessionLocal() as session:

        statement = (
            select(Song)
            .options(selectinload(Song.idols))
            .where(Song.id == song_id)
        )

        result = await session.execute(statement)
        song = result.scalar_one_or_none()

        if song is None:
            raise HTTPException(
                status_code=404,
                detail="Song not found"
            )

        return {
            "id": song.id,
            "title": song.title,
            "idol_ids": [
                idol.id for idol in song.idols
            ],
            "idol_names": [
                idol.name for idol in song.idols
            ]
        }
    
@app.get(
    "/idols/{idol_id}/songs",
    response_model=list[SongResponse]
)
async def get_idol_songs(idol_id: UUID):
    async with SessionLocal() as session:

        idol = await session.get(Idol, idol_id)

        if idol is None:
            raise HTTPException(
                status_code=404,
                detail="Idol not found"
            )

        statement = (
            select(Song)
            .join(Song.idols)
            .options(selectinload(Song.idols))
            .where(Idol.id == idol_id)
        )

        result = await session.execute(statement)
        songs = result.scalars().all()

        return [
            {
                "id": song.id,
                "title": song.title,
                "idol_ids": [
                    idol.id for idol in song.idols
                ],
                "idol_names": [
                    idol.name for idol in song.idols
                ]
            }
            for song in songs
        ]
        
@app.get(
    "/idols/{idol_id}/songs/{song_id}",
    response_model=SongResponse
)
async def get_idol_song(
    idol_id: UUID,
    song_id: UUID
):
    async with SessionLocal() as session:

        statement = (
            select(Song)
            .join(Song.idols)
            .options(selectinload(Song.idols))
            .where(
                Song.id == song_id,
                Idol.id == idol_id
            )
        )

        result = await session.execute(statement)
        song = result.scalar_one_or_none()

        if song is None:
            raise HTTPException(
                status_code=404,
                detail="Song not found for this idol"
            )

        return {
            "id": song.id,
            "title": song.title,
            "idol_ids": [
                idol.id for idol in song.idols
            ],
            "idol_names": [
                idol.name for idol in song.idols
            ]
        }