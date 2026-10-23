import pytest

@pytest.mark.asyncio
async def test_register_success(client):
    response = await client.post("/auth/register", json={"username": "Mikasa Ackerman", "email": "mikasaackerman@gmail.com", "password": "ereh835"})
    
    assert response.status_code == 201
    data = response.json()
    
    assert data["username"] == "Mikasa Ackerman"
    assert data["email"] == "mikasaackerman@gmail.com"
    assert "id" in data
    assert "password" not in data
    assert "password_hash" not in data
    
@pytest.mark.asyncio
async def test_duplicate_register(client):
    user = {"username": "Mikasa Ackerman", "email": "mikasaackerman@gmail.com", "password": "ereh835"}
    first_response = await client.post("/auth/register", json=user)
    
    second_response = await client.post("/auth/register", json=user)
    
    assert first_response.status_code == 201
    assert second_response.status_code == 409
    

@pytest.mark.asyncio
async def test_login_success(client):
    await client.post("/auth/register", json={"username": "Mikasa Ackerman", "email": "mikasaackerman@gmail.com", "password": "ereh835"})
    response = await client.post("/auth/login", data={"username": "Mikasa Ackerman", "password": "ereh835"})
    assert response.status_code == 200
    data = response.json()
    
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 0
    
@pytest.mark.asyncio
async def test_login_wrong_password(client):
    await client.post("/auth/register", json={"username": "Mikasa Ackerman", "email": "mikasaackerman@gmail.com", "password": "ereh835"})
    
    response = await client.post("/auth/login", data={"username": "Mikasa Ackerman", "password": "wrongpassword"})
    assert response.status_code == 401