import pytest

def test_valid_response(client):
    response = client.get('/groups/', follow=True)
    response_data = response.json()
    assert response.status_code == 200
    assert "@id" in response_data
    assert "groups" in response_data and isinstance(response.json().get("groups"), list)
    
    # Testing if the groups key's value is an empty list or a valid list
    is_empty = "groups" in response_data and len(response.json()["groups"]) == 0
    
    if not is_empty:
        group_keys = response.json()["groups"][0].keys()
        has_entries = "@id" in group_keys and "key" in group_keys and "name" in group_keys
    
    assert is_empty or has_entries

