import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from ipmanager.api.models import Group, IPRange


@pytest.fixture(autouse=True)
def plain_staticfiles(settings):
    """Render templates without the WhiteNoise manifest storage, which would
    otherwise require collectstatic to have run before the tests."""
    settings.STORAGES = {
        'staticfiles': {
            'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'
        }
    }


@pytest.fixture
def logged_in_client(client, db):
    """A client authenticated as an ordinary (non-superuser) UI user."""
    user = get_user_model().objects.create_user(username='tester', password='tester')
    client.force_login(user)
    return client


@pytest.fixture
def interleaved_groups(db):
    """Four groups whose keys alternate between matching and not matching
    the IP 192.168.1.5, so a key-only ordering is distinguishable from a
    containment-first ordering."""
    ranges = {
        'a-no': '10.0.0.0/8',
        'b-yes': '192.168.1.0/24',
        'c-no': '172.16.0.0/12',
        'd-yes': '192.168.0.0/16',
    }
    for key, value in ranges.items():
        group = Group.objects.create(key=key, name=key)
        IPRange.objects.create(group=group, value=value)


@pytest.mark.django_db
def test_groups_containing_test_ip_sort_first(logged_in_client, interleaved_groups):
    response = logged_in_client.get(
        reverse('list_all_groups'), {'test_ip': '192.168.1.5'}
    )

    assert response.status_code == 200
    group_list = response.context['group_list']
    assert [group.key for group in group_list] == ['b-yes', 'd-yes', 'a-no', 'c-no']
    assert [group.contained for group in group_list] == [True, True, False, False]


@pytest.mark.django_db
def test_groups_sort_by_key_without_test_ip(logged_in_client, interleaved_groups):
    response = logged_in_client.get(reverse('list_all_groups'))

    assert response.status_code == 200
    group_list = response.context['group_list']
    assert [group.key for group in group_list] == ['a-no', 'b-yes', 'c-no', 'd-yes']
