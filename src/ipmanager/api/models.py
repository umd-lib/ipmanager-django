# Create your models here.
from django.db.models import TextField, IntegerField, CharField, \
  BooleanField, CASCADE, ForeignKey, UniqueConstraint, IntegerChoices
from django_extensions.db.models import TimeStampedModel
from ipaddress import IPv4Network
from django.core.validators import RegexValidator
import re
from django.core.exceptions import ValidationError
from cidr.cidr import Cidr, CidrSet

class Group(TimeStampedModel):
  key = CharField(
    max_length=32, 
    unique=True, 
    validators=[RegexValidator(regex=r"\A[a-z][a-z\d_-]*\Z", flags=re.IGNORECASE)]
  )
  name = CharField(max_length=128, unique=True)
  description = TextField(blank=True)
  notes = TextField(blank=True)
  export = BooleanField(default=False)

  def __str__(self):
    return f"{self.name} ({self.key})"

  def __contains__(self, ip):
    return (self.ip_ranges_contain(ip) or self.includes(ip)) and not self.excludes(ip)

  def traverse(self, relation_type: int, root=None, groups=None):
    root = self
    
    if groups is None:
      groups = set()

    relations_list = Relation.objects.filter(subject=self, relation=relation_type)
    for relation_obj in relations_list:
      group = relation_obj.object
      if group != root and group not in groups:
        groups.add(group)
        groups.update(group.traverse(relation_type, root, groups))
    return groups

  def excludes(self, ip):
    excluded_groups = self.traverse(Relation.RelationType.EXCLUSION)
    
    for group in excluded_groups:
      if group.ip_ranges_contain(ip):
        return True
      
    return False
  
  def includes(self, ip):
    included_groups = self.traverse(Relation.RelationType.INCLUSION)
    
    for group in included_groups:
      if group.ip_ranges_contain(ip):
        return True
      
    return False

  def ip_ranges_contain(self, ip: str) -> bool:
    ip_address = Cidr(ip)
    ip_ranges_cidr = CidrSet()
    ip_ranges = IPRange.objects.filter(group=self)
    
    for ip_range in ip_ranges:
      ip_ranges_cidr.add(Cidr(ip_range.value))
      
    return ip_address in ip_ranges_cidr
  
def validate_ipv4_or_cidr_address(value):
  try :
    IPv4Network(value)
  except ValueError:
    raise ValidationError("IP or cidr address invalid.")

class IPRange(TimeStampedModel):
  group = ForeignKey(Group, on_delete=CASCADE)
  value = CharField(max_length=32, validators=[validate_ipv4_or_cidr_address])
  class Meta:
    constraints = [
      UniqueConstraint(fields=['group', 'value'], name='unique_group_ip_pair')
    ]   
  
  def __str__(self):
    return f"{self.group}: {self.value}"


class Relation(TimeStampedModel):
  class RelationType(IntegerChoices):
    INCLUSION = 0
    EXCLUSION = 1

  class Meta:
    constraints = [
      UniqueConstraint(fields=['subject', 'object'], name='unique_subject_object_relation_pair')
    ] 

  subject = ForeignKey(Group, on_delete=CASCADE, related_name="relation_subjects")
  object = ForeignKey(Group, on_delete=CASCADE, related_name="relation_objects")
  relation = IntegerField(choices=RelationType) 

  def clean(self):
    if (self.subject == self.object):
      raise ValidationError("Subject and Object group cannot be the same.")
  
  def __str__(self):
    return f"{self.subject} {"includes" if self.relation == Relation.RelationType.INCLUSION else "excludes"} {self.object}"


