from django.forms import CharField, Form, HiddenInput, ModelForm, Textarea

from ipmanager.api.models import IPRange, Relation, Note

class RelationForm(ModelForm):
    class Meta:
        model = Relation
        fields = ['subject', 'object', 'relation']
        widgets = {
            'subject': HiddenInput(),
        }


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['user', 'content', 'group']
        widgets = {
            'user': HiddenInput(),
            'group': HiddenInput(),
            'content': Textarea(attrs={'cols': 60, 'rows': 2})
        }


class IPRangeForm(ModelForm):
    class Meta:
        model = IPRange
        fields = ['group', 'value']
        widgets = {
            'group': HiddenInput(),
        }


class TestIPForm(Form):
    test_ip = CharField(max_length=32, label="Test IP")
