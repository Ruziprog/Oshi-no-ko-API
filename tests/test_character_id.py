def test_character_by_id(client, auth_headers):
    response = client.post("/characters", json={
        "name": "Goida Satoru",
        "age": 28,
        "description": "The honored One",
        "role": "GOIDAAAAAAAAA!"
    }, headers=auth_headers)
    
    response = client.get(f"/characters/{response.json()['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Goida Satoru"