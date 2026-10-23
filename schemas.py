
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, EmailStr


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=72)
    email: EmailStr


class UserLogin(BaseModel):
    username: str
    password: str


class CharacterCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    age: int = Field(ge=0)
    description: str | None = Field(default=None, max_length=200)
    role: str | None = Field(default=None, max_length=50)


class CharacterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    age: int
    description: str | None = None
    role: str | None = None


class SongCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    idol_ids: list[UUID] = Field(default_factory=list)


class SongResponse(BaseModel):
    id: UUID
    title: str
    idol_ids: list[UUID]
    idol_names: list[str]
