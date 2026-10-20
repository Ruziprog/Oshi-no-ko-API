import pytest
from pydantic import ValidationError
from schemas import CharacterCreate

@pytest.fixture
def valid_character_data():
    return {
        "name": "Ruby Hoshino",
        "age": 16,
        "description": "Idol",
        "role": "Main character",
    }
    
@pytest.mark.parametrize("age", [16, 17, 18])
def test_character_create_accepts_valid_data(age, valid_character_data):
    data = valid_character_data.copy()
    data["age"] = age
    character = CharacterCreate(**data)
    assert character.name == "Ruby Hoshino"
    assert character.age == age

def test_character_create_rejects_missing_age(valid_character_data):
    data = valid_character_data.copy()
    del data["age"]
    with pytest.raises(ValidationError):
        CharacterCreate(**data)
    
def test_character_create_missing_name(valid_character_data):
    data = valid_character_data.copy()
    del data["name"]
    with pytest.raises(ValidationError):
        CharacterCreate(**data)
        
def test_character_create_rejects_negative_age(valid_character_data):
    data = valid_character_data.copy()
    data["age"] = -1
    with pytest.raises(ValidationError):
        CharacterCreate(**data)