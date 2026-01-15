# Create your models here.
import re
from ipaddress import IPv4Network
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    ForeignKey,
    IntegerChoices,
    IntegerField,
    TextField,
    UniqueConstraint,
)
from django_extensions.db.models import TimeStampedModel

from ipmanager.core.cidr import Cidr, CidrSet

from django.contrib.auth import get_user_model


class Group(TimeStampedModel):
    key = CharField(
        max_length=32,
        unique=True,
        validators=[RegexValidator(regex=r'\A[a-z][a-z\d_-]*\Z', flags=re.IGNORECASE)],
    )
    name = CharField(max_length=128, unique=True)
    description = TextField(blank=True)
    export = BooleanField(default=False)

    def __str__(self):
        return f'{self.name} ({self.key})'

    def __contains__(self, ip) -> bool:
        return Cidr(ip) in self.collect()

    def collect(self) -> CidrSet:
        internal = CidrSet()

        # Adds all IP addresses that directly belong to the current group
        # to a CidrSet
        for iprange in IPRange.objects.filter(group=self):
            internal.add(Cidr(iprange.value))

        included = CidrSet()
        excluded = CidrSet()

        # Adds all addresses to the included set if the relation is INCLUSION
        # all excluded IP addresses to the excluded setobj
        for relation_obj in Relation.objects.filter(subject=self):
            if relation_obj.relation == Relation.RelationType.INCLUSION:
                included += relation_obj.object.collect()
            else:
                excluded += relation_obj.object.collect()

        # combines group's own ip addresses and all of its included group's ipaddresses
        # removes any excluded ip addresses from the union above
        return (internal + included) - excluded


def validate_ipv4_or_cidr_address(value):
    try:
        IPv4Network(value)
    except ValueError:
        raise ValidationError('IP or cidr address invalid.')


class IPRange(TimeStampedModel):
    group = ForeignKey(Group, on_delete=CASCADE)
    value = CharField(max_length=32, validators=[validate_ipv4_or_cidr_address])

    class Meta:
        constraints = [
            UniqueConstraint(fields=['group', 'value'], name='unique_group_ip_pair')
        ]

    def __str__(self):
        return f'{self.group}: {self.value}'


class Relation(TimeStampedModel):
    class RelationType(IntegerChoices):
        INCLUSION = 0
        EXCLUSION = 1

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['subject', 'object'], name='unique_subject_object_relation_pair'
            )
        ]

    subject = ForeignKey(Group, on_delete=CASCADE, related_name='relation_subjects')
    object = ForeignKey(Group, on_delete=CASCADE, related_name='relation_objects')
    relation = IntegerField(choices=RelationType)

    def clean(self):
        if self.subject == self.object:
            raise ValidationError('Subject and Object group cannot be the same.')

    def __str__(self):
        return f'{self.subject} {"includes" if self.relation == Relation.RelationType.INCLUSION else "excludes"} {self.object}'

class Note(TimeStampedModel):
    user = ForeignKey(get_user_model(), on_delete=CASCADE)
    content = TextField()
    group = ForeignKey(Group, on_delete=CASCADE)

    def __str__(self):
        return f'{self.created.strftime("%Y-%m-%d %H:%M:%S")} [{self.user.username}]: {self.content}'

# we want this 2025-01-02T16:29:43Z
