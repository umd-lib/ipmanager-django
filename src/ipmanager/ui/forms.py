from django.forms import ModelForm, HiddenInput
from ipmanager.api.models import IPRange

class IPRangeForm(ModelForm):
  class Meta:
    model = IPRange
    fields = ['group', 'value']
    widgets = {
      'group': HiddenInput(),
    }
