import pytest

def test_valid_response(client):
    response = client.get('/groups/', follow=True)
    response_data = response.json()
    assert response.status_code == 200
    assert "@id" in response_data
    assert "groups" in response_data and isinstance(response_data.get("groups"), list)
    
    # Testing if the groups key's value is an empty list or a valid list
    is_empty = "groups" in response_data and len(response_data["groups"]) == 0
    
    if not is_empty:
        group_data = response_data["groups"][0]
        has_entries = "@id" in group_data and "key" in group_data and "name" in group_data
    
    assert is_empty or has_entries

