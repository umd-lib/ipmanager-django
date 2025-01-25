import pytest
from django.core.exceptions import ValidationError

from ipmanager.api.models import Group, IPRange


@pytest.mark.django_db
def test_valid_fields():
    group1 = Group(key='aBCD123-', name='the group')
    group1.save()
    iprange = IPRange(group=Group.objects.get(name='the group'), value='192.168.1.1/12')
    iprange.save()
    assert iprange.group == group1
    assert iprange.value == '192.168.1.1/12'


@pytest.mark.django_db
def test_no_group():
    iprange = IPRange(value='192.168.1.1')

    with pytest.raises(ValidationError) as err:
        iprange.full_clean()


@pytest.mark.django_db
def test_no_value():
    group1 = Group(key='aBCD123-', name='the group')
    group1.save()
    iprange = IPRange(group=Group.objects.get(name='the group'))

    with pytest.raises(ValidationError) as err:
        iprange.full_clean()


@pytest.mark.django_db
def test_value_too_long():
    group1 = Group(key='aBCD123-', name='the group')
    group1.save()
    iprange = IPRange(
        group=Group.objects.get(name='the group'),
        value='192.168.134.123123123123123123123',
    )

    with pytest.raises(ValidationError) as err:
        iprange.full_clean()


@pytest.mark.django_db
def test_value_invalid_ip():
    group1 = Group(key='aBCD123-', name='the group')
    group1.save()
    iprange = IPRange(group=Group.objects.get(name='the group'), value='192.1')

    with pytest.raises(ValidationError) as err:
        iprange.full_clean()


@pytest.mark.django_db
def test_group_value_pair_not_unique():
    group1 = Group(key='aBCD123-', name='the group')
    group1.save()
    iprange1 = IPRange(group=Group.objects.get(name='the group'), value='192.168.1.1')
    iprange1.save()
    iprange2 = IPRange(group=Group.objects.get(name='the group'), value='192.168.1.1')

    with pytest.raises(ValidationError) as err:
        iprange2.full_clean()


@pytest.mark.django_db
def test_delete_group_deletes_ipranges():
    group1 = Group(key='aBCD123-', name='the group')
    group1.save()
    iprange1 = IPRange(group=Group.objects.get(name='the group'), value='192.168.1.1')
    iprange2 = IPRange(group=Group.objects.get(name='the group'), value='192.168.1.2')
    iprange1.save()
    iprange2.save()
    group1.delete()

    assert len(IPRange.objects.all()) == 0
