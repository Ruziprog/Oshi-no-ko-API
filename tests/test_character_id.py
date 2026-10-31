
import pytest


@pytest.mark.asyncio
async def test_character_by_id(client, auth_headers):
    response = await client.post(
        "/characters",
        json={
            "name": "Goida Satoru",
            "age": 28,
            "description": "The honored One",
            "role": "GOIDAAAAAAAAA!",
        },
        headers=auth_headers,
    )

    assert response.status_code == 201

    character_id = response.json()["id"]

    response = await client.get(f"/characters/{character_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Goida Satoru"
