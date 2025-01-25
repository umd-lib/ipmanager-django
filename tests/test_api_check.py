import pytest

from ipmanager.api.models import Group, IPRange


# from src.ipmanager.api.views import APICheckView
@pytest.mark.django_db
def test_missing_ip(client):
    response = client.get('/check', {'notIP': '123.123.1'}, follow=True)
    assert response.status_code == 400


@pytest.mark.django_db
def test_group_present_ip_absent(client):
    response = client.get('/check', {'group': 'A', 'notIP': '123.123.1'}, follow=True)
    assert response.status_code == 400


@pytest.mark.django_db
def test_unparseable_ip(client):
    response = client.get('/check', {'ip': '192.8888999'}, follow=True)
    # Checking f-string for unparseable ip_address
    assert (
        response.json()['detail']
        == "The value 192.8888999 you provided in the 'ip' query parameter cannot be parsed as a valid IP address."
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_group_not_found(client):
    response = client.get(
        '/check', {'group': 'notFound', 'ip': '192.168.0.1'}, follow=True
    )
    assert response.status_code == 404


@pytest.mark.django_db
def test_correct_group_and_ip(client):
    group = Group(key='A', name='a group')
    group.save()
    iprange = IPRange(group=Group.objects.get(name='a group'), value='192.168.0.1')
    iprange.save()
    response = client.get('/check', {'group': 'A', 'ip': '192.168.0.1'}, follow=True)
    assert response.status_code == 200

    response_data = response.json()
    # Checking if the response has the group key and ip_address that was passed
    # in as query parameter
    assert response_data['group']['key'] == 'A'
    assert response_data['ip'] == '192.168.0.1'

    # To check if the contained function works as intended
    assert response_data['contained'] == True


@pytest.mark.django_db
def test_correct_ip_only(client):
    group = Group(key='abc', name='A')
    group.save()
    iprange = IPRange(group=Group.objects.get(name='A'), value='192.168.0.1')
    iprange.save()
    response = client.get('/check', {'ip': '192.168.0.1'}, follow=True)
    assert response.json()['ip'] == '192.168.0.1'
