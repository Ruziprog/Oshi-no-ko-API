from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import select
from deps import get_current_user

from schemas import UserCreate, UserLogin
from models import User
from database import SessionLocal
from security import (
    hash_password,
    verify_password,
    create_access_token,
)
from models import User, Character
from schemas import (
    UserCreate,
    UserLogin,
    CharacterCreate,
    CharacterResponse,
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
async def login(user: UserLogin):
    async with SessionLocal() as session:
        statement = select(User).where(User.username == user.username)
        result = await session.execute(statement)
        db_user = result.scalar_one_or_none()

        if db_user is None:
            raise HTTPException(status_code=400, detail="Invalid username or password")

        if not verify_password(user.password, db_user.password_hash):
            raise HTTPException(status_code=400, detail="Invalid username or password")

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
    "/characters/{character_name}",
    response_model=CharacterResponse
)
async def get_character(character_name: str):
    async with SessionLocal() as session:
        statement = select(Character).where(
            Character.name == character_name
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
async def create_character(character: CharacterCreate):
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
    character_id: int,
    character_data: CharacterCreate
):
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
async def delete_character(character_id: int):
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