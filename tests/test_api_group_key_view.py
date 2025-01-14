import pytest

def test_valid_group_key(client):
    response = client.get("/groups/key1", follow=True)
    assert response.status_code == 200
    assert "@id" in response.json()
    assert response.json()["key"] == "key1"
    assert response.json()["name"] == "group key1's name"

def test_invalid_group_key(client):
    response = client.get("/groups/key20", follow=True)
    assert response.status_code == 404
    assert response.json()["title"] == "Group not found"
    assert "detail" in response.json()