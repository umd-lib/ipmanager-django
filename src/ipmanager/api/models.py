# Create your models here.
from django.db.models import TextField, IntegerField, CharField, \
  BooleanField, CASCADE, ForeignKey, UniqueConstraint, IntegerChoices
from django_extensions.db.models import TimeStampedModel
from ipaddress import IPv4Network
from django.core.validators import RegexValidator
import re
from django.core.exceptions import ValidationError

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
  
def validate_ipv4_or_cidr_address(value):
  try :
    IPv4Network(value)
    return True
  except ValueError:
    return False

class IPRange(TimeStampedModel):
  group = ForeignKey(Group, on_delete=CASCADE)
  value = CharField(max_length=64, validators=[validate_ipv4_or_cidr_address])
  class Meta:
    constraints = [
      UniqueConstraint(fields=['group', 'value'], name='unique_group_ip_pair')
    ]   

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