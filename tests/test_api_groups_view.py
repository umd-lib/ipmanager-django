import pytest

from ipmanager.api.models import Group


@pytest.mark.django_db
def test_valid_response_with_exported_groups(client):
    # Creating test data
    group1 = Group(key='group1', name='group1', export=True)
    group1.save()

    response = client.get('/groups/', follow=True)
    response_data = response.json()
    assert response.status_code == 200
    assert '@id' in response_data
    assert 'groups' in response_data and isinstance(response_data.get('groups'), list)

    # Testing if the groups key's value is a valid list
    group_data = response_data['groups'][0]
    assert '@id' in group_data and 'key' in group_data and 'name' in group_data
    assert group_data['key'] == 'group1' and group_data['name'] == 'group1'


@pytest.mark.django_db
def test_valid_response_with_no_exported_groups(client):
    response = client.get('/groups/', follow=True)
    response_data = response.json()
    assert response.status_code == 200
    assert '@id' in response_data
    assert 'groups' in response_data and isinstance(response_data.get('groups'), list)

    # Testing if the groups key's value is an empty list
    assert len(response_data['groups']) == 0
