from pydantic import BaseModel
from uuid import UUID

class UserCreate(BaseModel):
    username: str
    password: str
    email: str

class UserLogin(BaseModel):
    username: str
    password: str


class CharacterCreate(BaseModel):
    name: str
    age: int | None = None
    description: str | None = None
    role: str | None = None

class CharacterResponse(BaseModel):
    id: UUID
    name: str
    age: int
    description: str
    role: str
    
    
class SongCreate(BaseModel):
    title: str
    idol_ids: list[UUID]


class SongResponse(BaseModel):
    id: UUID
    title: str
    idol_ids: list[UUID]
    idol_name: list[str]