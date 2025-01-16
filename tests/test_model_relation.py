import pytest
from ipmanager.api.models import Group, Relation
from django.core.exceptions import ValidationError

@pytest.mark.django_db
def test_valid_fields():
    # Testing if a Relation can be created with all valid fields present
    subject_group = Group(key="aABCD-subject", name="valid_subject_Group")
    object_group = Group(key="aABCD-object", name="valid_object_Group")
    
    subject_group.save()
    object_group.save()

    relation_obj = Relation(
        subject=Group.objects.get(name="valid_subject_Group"),
        object=Group.objects.get(name="valid_object_Group"),
        relation=Relation.RelationType.INCLUSION
    )
    relation_obj.save()

    assert relation_obj.subject == subject_group
    assert relation_obj.object == object_group
    assert relation_obj.relation == Relation.RelationType.INCLUSION

@pytest.mark.django_db
def test_same_subject_and_object():
    # Testing if a ValidationError is raised when subject and 
    # object are the same Group
    same_group = Group(key="aABCD-same-group", name="valid_same_group")
    same_group.save()

    relation_obj = Relation(
        subject=Group.objects.get(name="valid_same_group"),
        object=Group.objects.get(name="valid_same_group"),
        relation=Relation.RelationType.INCLUSION
    )
    with pytest.raises(ValidationError) as err:
        relation_obj.full_clean()

@pytest.mark.django_db
def test_undefined_relation_type():
    # Testing if a ValidationError is raised when the relation 
    # field is an invalid choice
    subject_group = Group(key="aABCD-subject", name="valid_subject_Group")
    object_group = Group(key="aABCD-object", name="valid_object_Group")
    
    subject_group.save()
    object_group.save()

    relation_obj = Relation(
        subject=Group.objects.get(name="valid_subject_Group"),
        object=Group.objects.get(name="valid_object_Group"),
        relation=3
    )
    with pytest.raises(ValidationError) as err:
        relation_obj.full_clean()
    
@pytest.mark.django_db
def test_same_subject_object_combination():
    # Testing if a ValidationError is raised when 2 Relations 
    # have the same subject and object
    subject_group = Group(key="aABCD-subject", name="valid_subject_Group")
    object_group = Group(key="aABCD-object", name="valid_object_Group")

    subject_group.save()
    object_group.save()

    relation_obj = Relation(
        subject=Group.objects.get(name="valid_subject_Group"),
        object=Group.objects.get(name="valid_object_Group"),
        relation=Relation.RelationType.INCLUSION
    )
    relation_obj.save()

    relation_obj2 = Relation(
        subject=Group.objects.get(name="valid_subject_Group"),
        object=Group.objects.get(name="valid_object_Group"),
        relation=Relation.RelationType.EXCLUSION
    )

    with pytest.raises(ValidationError) as err:
        relation_obj2.full_clean()

@pytest.mark.django_db
def test_missing_subject():
    # Testing if a Relation cannot be created when it's missing a subject field
    object_group = Group(key="aABCD-object", name="valid_object_Group")

    object_group.save()

    relation_obj = Relation(
        object=Group.objects.get(name="valid_object_Group"),
        relation=Relation.RelationType.INCLUSION
    )

    with pytest.raises(Relation.subject.RelatedObjectDoesNotExist) as err:
        relation_obj.full_clean()

@pytest.mark.django_db
def test_same_subject_different_objects_combination():
    # Test for adding two valid subject-object group pairs, where 
    # the subject group is same but object groups are different
    subject_group = Group(key="aABCD-subject", name="valid_subject_Group")
    object_group1 = Group(key="aABCD-object-1", name="valid_object_Group-1")
    object_group2 = Group(key="aABCD-object-2", name="valid_object_Group-2")

    subject_group.save()
    object_group1.save()
    object_group2.save()

    relation_obj_1 = Relation(
        subject=Group.objects.get(name="valid_subject_Group"),
        object=Group.objects.get(name="valid_object_Group-1"),
        relation=Relation.RelationType.INCLUSION
    )
    relation_obj_1.save()

    relation_obj_2 = Relation(
        subject=Group.objects.get(name="valid_subject_Group"),
        object=Group.objects.get(name="valid_object_Group-2"),
        relation=Relation.RelationType.EXCLUSION
    )

    relation_obj_2.save()

    assert relation_obj_1.object.name == "valid_object_Group-1"
    assert relation_obj_2.object.name == "valid_object_Group-2"

@pytest.mark.django_db
def test_deleting_group_present_in_two_relations():
    # Testing if all relations that reference the same group get deleted 
    # when the group is deleted
    group1 = Group(key="aABCD-group1", name="valid_Group-1")
    group2 = Group(key="aABCD-group2", name="valid_Group-2")

    group1.save()
    group2.save()

    relation_obj_1 = Relation(
        subject=Group.objects.get(name="valid_Group-1"),
        object=Group.objects.get(name="valid_Group-2"),
        relation=Relation.RelationType.INCLUSION
    )
    relation_obj_1.save()

    relation_obj_2 = Relation(
        subject=Group.objects.get(name="valid_Group-2"),
        object=Group.objects.get(name="valid_Group-1"),
        relation=Relation.RelationType.EXCLUSION
    )
    relation_obj_2.save()

    assert len(Relation.objects.all()) == 2
    group1.delete()
    assert len(Relation.objects.all()) == 0