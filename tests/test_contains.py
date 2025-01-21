import pytest
from ipmanager.api.models import Group, IPRange, Relation

# @pytest.mark.django_db
# def test_contains_ip():
#   group1 = Group(key="A", name="A")
#   group1.save()
#   ip1 = IPRange(group=group1, value="0.0.0.0/24")
#   ip1.save()

#   ip2 = "0.0.0.1"
#   assert group1.ip_ranges_contain(ip2)

@pytest.mark.django_db
def test_traverse():
  """tests if the traverse method generates the right set of groups"""
  group1 = Group(key="A", name="A")
  group2 = Group(key="B", name="B")
  group3 = Group(key="C", name="C")
  group4 = Group(key="D", name="D")
  group1.save()
  group2.save()
  group3.save()
  group4.save()
  relation1 = Relation(subject=group1, object=group2, relation=Relation.RelationType.INCLUSION)
  relation2 = Relation(subject=group1, object=group3, relation=Relation.RelationType.INCLUSION)
  relation3 = Relation(subject=group2, object=group4, relation=Relation.RelationType.INCLUSION)
  relation1.save()
  relation2.save()
  relation3.save()
  expected = {group2, group3, group4}
  assert expected == group1.traverse(Relation.RelationType.INCLUSION)

@pytest.mark.django_db
def test_includes():
  """tests if an iprange can be found in a groups included groups"""
  group1 = Group(key="A", name="A")
  group2 = Group(key="B", name="B")
  group1.save()
  group2.save()
  ip1 = IPRange(group=group1, value="10.204.145.0")
  ip1.save()
  ip2 = IPRange(group=group2, value="10.204.145.0")
  ip2.save()
  ip = "10.204.145.0"
  relation1 = Relation(subject=group1, object=group2, relation=Relation.RelationType.INCLUSION)
  relation1.save()
  
  assert ip in group1
  
@pytest.mark.django_db
def test_excludes():
  """tests that exlusion overrides inclusion"""
  group1 = Group(key="A", name="A")
  group1.save()
  group2 = Group(key="B", name="B")
  group2.save()
  group3 = Group(key="C", name="C")
  group3.save()
  ip1 = IPRange(group=group1, value="10.204.145.0")
  ip1.save()
  ip2 = IPRange(group=group2, value="10.204.145.1")
  ip2.save()
  ip3 = IPRange(group=group3, value="10.204.145.1")
  ip3.save()
  relation_exclude = Relation(
    subject=group1, 
    object=group2, 
    relation=Relation.RelationType.EXCLUSION
    )
  relation_exclude.save()
  relation_include = Relation(
    subject=group1,
    object=group3,
    relation=Relation.RelationType.INCLUSION
  )
  relation_include.save()

  assert "0.0.0.0" not in group1

@pytest.mark.django_db
def test_cidr():
  """tests cidr notation"""
  group = Group(key="A", name="A")
  group.save()
  ip = IPRange(group=group, value="10.204.145.0/24")
  ip.save()

  assert "10.204.145.2" in group

