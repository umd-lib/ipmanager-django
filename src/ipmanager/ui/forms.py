from django.forms import ModelForm, HiddenInput, Form, CharField
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
class TestIPForm(Form):
    test_ip = CharField(max_length=32)