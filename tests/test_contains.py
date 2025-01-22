import pytest
from ipmanager.api.models import Group, IPRange, Relation

@pytest.mark.django_db
def test_A_includes_B():
  """tests if an iprange can be found in a group's included groups"""
  group1 = Group(key="A", name="A")
  group2 = Group(key="B", name="B")
  group1.save()
  group2.save()
  ip1 = IPRange(group=group1, value="10.204.145.1")
  ip1.save()
  ip2 = IPRange(group=group2, value="10.204.145.0")
  ip2.save()
  ip = "10.204.145.0"
  relation1 = Relation(subject=group1, object=group2, relation=Relation.RelationType.INCLUSION)
  relation1.save()
  
  assert ip in group1
  
@pytest.mark.django_db
def test_A_excludes_B():
  """tests that an excluded ip range isn't found in its parent"""
  group1 = Group(key="A", name="A")
  group2 = Group(key="B", name="B")
  group1.save()
  group2.save()
  ip1 = IPRange(group=group1, value="10.204.145.0")
  ip1.save()
  ip2 = IPRange(group=group2, value="10.204.145.0")
  ip2.save()
  ip = "10.204.145.0"
  relation1 = Relation(subject=group1, object=group2, relation=Relation.RelationType.EXCLUSION)
  relation1.save()
  
  assert ip not in group1

@pytest.mark.django_db
def test_A_includes_B_B_includes_C():
  """ tests that an IP range in group C can be included in group A,
  because A includes B and B includes C"""
  group1 = Group(key="A", name="A")
  group2 = Group(key="B", name="B")
  group3 = Group(key="C", name="C")
  group1.save()
  group2.save()
  group3.save()
  ip1 = IPRange(group=group1, value="10.204.145.0")
  ip1.save()
  ip2 = IPRange(group=group2, value="10.204.145.1")
  ip2.save()
  ip3 = IPRange(group=group3, value="10.204.145.2")
  ip3.save()
  relation1 = Relation(subject=group1, object=group2, relation=Relation.RelationType.INCLUSION)
  relation1.save()
  relation2 = Relation(subject=group2, object=group3, relation=Relation.RelationType.INCLUSION)
  relation2.save()
  ip = ip3.value
  assert ip in group1

@pytest.mark.django_db
def test_A_excludes_B_B_excludes_C():
  """ tests that an IP range in group C can be excluded from group A,
  because A excludes B and B excludes C"""
  group1 = Group(key="A", name="A")
  group2 = Group(key="B", name="B")
  group3 = Group(key="C", name="C")
  group1.save()
  group2.save()
  group3.save()
  ip1 = IPRange(group=group1, value="192.3.0.0/24")
  ip1.save()
  ip2 = IPRange(group=group2, value="192.3.1.0/24")
  ip2.save()
  ip3 = IPRange(group=group3, value="192.3.1.2")
  ip3.save()
  relation1 = Relation(subject=group1, object=group2, relation=Relation.RelationType.EXCLUSION)
  relation1.save()
  relation2 = Relation(subject=group2, object=group3, relation=Relation.RelationType.EXCLUSION)
  relation2.save()
  ip = ip3.value
  assert ip not in group1
  
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

@pytest.mark.django_db
def test_excludes_issue():
  # LIBITD-2170 issue
  world = Group(key="world", name="world")
  single_ip = Group(key="single_ip", name="single_ip")
  includes_single_ip = Group(key="includes_single_ip", name="includes_single_ip")
  group = Group(key="group", name="group")
  world.save()
  single_ip.save()
  includes_single_ip.save()
  group.save()

  ip1 = IPRange(group=world, value="0.0.0.0/0")
  ip1.save()
  ip2 = IPRange(group=single_ip, value="192.168.0.2")
  ip2.save()
  
  rel1 = Relation(subject=includes_single_ip, object=single_ip, relation=Relation.RelationType.INCLUSION)
  rel1.save()
  rel2 = Relation(subject=group, object=world, relation=Relation.RelationType.INCLUSION)
  rel2.save()
  rel3 = Relation(subject=group, object=includes_single_ip, relation=Relation.RelationType.EXCLUSION)
  rel3.save()
  
  assert "192.168.0.2" not in group

@pytest.mark.django_db
def test_nested_inclusion():
  """tests inclusion when there is a long chain of inclusions"""
  group1 = Group(key="A", name="A")
  group1.save()
  group2 = Group(key="B", name="B")
  group2.save()
  group3 = Group(key="C", name="C")
  group3.save()
  group4 = Group(key="D", name="D")
  group4.save()
  ip = IPRange(group=group4, value="10.204.145.0")
  ip.save()
  relation2in1= Relation(
    subject=group1, 
    object=group2, 
    relation=Relation.RelationType.INCLUSION
    )
  relation2in1.save()
  relation3in1 = Relation(
    subject=group1,
    object=group3,
    relation=Relation.RelationType.INCLUSION
  )
  relation3in1.save()
  relation4in1= Relation(
    subject=group1, 
    object=group4, 
    relation=Relation.RelationType.INCLUSION
    )
  relation4in1.save()
  assert "10.204.145.0" in group1

@pytest.mark.django_db
def test_excluded_farther_down_chain():
  """tests that the manager respects excluded IP addresses when 
    excluded group is far down the chain, ticket 2280"""
  ip = "129.2.19.99"
  films_group = Group(key="films", name="Films@UM")
  films_group.save()
  shady_grove_group = Group(key="shady-grove-umfilms", name="Films@UM, Shady Grove")
  shady_grove_group.save()
  um_group = Group(key="um", name="UMD College Park campus and VPN")
  um_group.save()
  usmai_group = Group(key="usmai-ezproxy", name="USMAI EZProxy")
  usmai_group.save()

  ip_um = IPRange(group=um_group, value=ip)
  ip_um.save()
  ip_usmai = IPRange(group=usmai_group, value=ip)
  ip_usmai.save()

  relation_shady_in_films= Relation(
    subject=films_group, 
    object=shady_grove_group, 
    relation=Relation.RelationType.INCLUSION
    )
  relation_shady_in_films.save()
  relation_um_in_films= Relation(
    subject=films_group, 
    object=um_group, 
    relation=Relation.RelationType.INCLUSION
    )
  relation_um_in_films.save()
  relation_usmai_not_in_um= Relation(
    subject=um_group, 
    object=usmai_group, 
    relation=Relation.RelationType.EXCLUSION
    )
  relation_usmai_not_in_um.save()

  assert ip not in films_group

@pytest.mark.django_db
def test_exclusion_with_inclusion():
  """A excludes B and B includes C so everything in C should be excluded from A"""
  groupA = Group(key="A", name="A")
  groupA.save()
  groupB = Group(key="B", name="B")
  groupB.save()
  groupC = Group(key="C", name="C")
  groupC.save()

  ipA1 = IPRange(group=groupA, value="192.168.1.1/24")
  ipA1.save()
  ipA2 = IPRange(group=groupA, value="192.168.2.1")
  ipA2.save()
  ipC = IPRange(group=groupC, value="192.168.2.1/24")
  ipC.save()

  rel1 = Relation(subject=groupA, object=groupB, relation=Relation.RelationType.EXCLUSION)
  rel1.save()
  rel2 = Relation(subject=groupB, object=groupC, relation=Relation.RelationType.INCLUSION)
  rel2.save()

  assert "192.168.2.1" not in groupA
