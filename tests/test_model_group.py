import pytest
from django.core.exceptions import ValidationError

from ipmanager.api.models import Group


@pytest.mark.django_db
def test_valid_fields():
    group = Group(
        key='aBCD123-',
        name='valid_group',
        description='Small Description',
        notes='No Notes',
    )

    group.save()
    assert group.key == 'aBCD123-'
    assert group.name == 'valid_group'
    assert group.description == 'Small Description'
    assert group.notes == 'No Notes'
    assert group.export == False


@pytest.mark.django_db
def test_invalid_key_regex():
    group = Group(key='123;*djs', name='valid_group')

    with pytest.raises(ValidationError) as err:
        group.full_clean()


@pytest.mark.django_db
def test_invalid_key_length():
    # This invalid_key is longer than max_length parameter of CharField
    invalid_key = 'a8BcD1eFgH2IjK3LmNoP4QrStUvWxY5Zz6'
    group = Group(key=invalid_key, name='valid_group')

    with pytest.raises(ValidationError) as err:
        group.full_clean()


@pytest.mark.django_db
def test_not_unique_key():
    group1 = Group(key='aBCD123-', name='valid_group')
    group1.save()
    group2 = Group(key='aBCD123-', name='in_valid_group')

    with pytest.raises(ValidationError) as err:
        group2.full_clean()


@pytest.mark.django_db
def test_no_key():
    group = Group(name='valid_group')

    with pytest.raises(ValidationError) as err:
        group.full_clean()


@pytest.mark.django_db
def test_invalid_name_length():
    group = Group(
        key='abc',
        name='invalid_group_name_is_too_long_invalid_group_name_is_too_long_invalid_group_name_is_too_long_invalid_group_name_is_too_long_too_long',
    )

    with pytest.raises(ValidationError) as err:
        group.full_clean()


@pytest.mark.django_db
def test_name_not_unique():
    group1 = Group(key='validKey1', name='Same Name')
    group1.save()
    group2 = Group(key='validKey2', name='Same Name')

    with pytest.raises(ValidationError) as err:
        group2.full_clean()


@pytest.mark.django_db
def test_no_name():
    group = Group(key='123')

    with pytest.raises(ValidationError) as err:
        group.full_clean()
