from django import forms

from .person_forms import PersonForm
from ..models import Author

class AuthorForm(PersonForm):
    class Meta(PersonForm.Meta):
        model = Author
        fields = PersonForm.Meta.fields + ['alias']
        widgets = {
            **PersonForm.Meta.widgets,
            'alias': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        data = super().clean()
        rnc = data['rnc']

        instance_pk = self.instance.pk if self.instance else None

        if Author.objects.filter(rnc=rnc).exclude(pk=instance_pk).exists():
            self.add_error('rnc', 'RNC already exists')
        
        return data