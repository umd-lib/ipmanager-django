from django.forms import ModelForm, HiddenInput
from ipmanager.api.models import Relation

class RelationForm(ModelForm):
  class Meta:
    model = Relation
    fields = ['subject', 'object', 'relation']
    widgets = {
      'subject' : HiddenInput(),
    }