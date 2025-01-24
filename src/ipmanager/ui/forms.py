from django.forms import ModelForm, HiddenInput
from ipmanager.api.models import IPRange, Relation

class RelationForm(ModelForm):
  class Meta:
    model = Relation
    fields = ['subject', 'object', 'relation']
    widgets = {
      'subject' : HiddenInput(),
    }


class IPRangeForm(ModelForm):
  class Meta:
    model = IPRange
    fields = ['group', 'value']
    widgets = {
      'group': HiddenInput(),
    }