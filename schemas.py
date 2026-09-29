from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    email: str

class UserLogin(BaseModel):
    username: str
    password: str


class CharacterCreate(BaseModel):
    name: str
    age: int
    description: str
    role: str

class CharacterResponse(BaseModel):
    id: int
    name: str
    age: int
    description: str
    role: str
    
    
class SongCreate(BaseModel):
    title: str
    idol_id: int


class SongResponse(BaseModel):
    id: int
    title: str
    idol_id: int
    idol_name: str