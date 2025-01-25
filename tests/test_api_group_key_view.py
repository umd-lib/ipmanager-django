import pytest

from ipmanager.api.models import Group


@pytest.mark.django_db
def test_valid_group_key(client):
    group = Group(key='abc', name='a group')
    group.save()
    response = client.get('/groups/abc', follow=True)
    assert response.status_code == 200
    assert '@id' in response.json()
    assert response.json()['key'] == 'abc'
    assert response.json()['name'] == 'a group'


@pytest.mark.django_db
def test_invalid_group_key(client):
    response = client.get('/groups/abcd', follow=True)
    assert response.status_code == 404
    assert response.json()['title'] == 'Group not found'
    assert 'detail' in response.json()
