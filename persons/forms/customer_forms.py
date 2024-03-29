from django import forms

from .person_forms import PersonForm
from ..models import Customer

class CustomerForm(PersonForm):
    class Meta(PersonForm.Meta):
        model = Customer
        fields = PersonForm.Meta.fields + ['library', 'credit_time', 'status']
        widgets = {
            **PersonForm.Meta.widgets,
            'library': forms.Select(attrs={'class': 'form-control'}),
            'credit_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        data = super().clean()
        rnc = data['rnc']
        library = data['library']
        instance_pk = self.instance.pk if self.instance else None

        if Customer.objects.filter(rnc=rnc, library=
                                   library).exclude(pk=instance_pk).exists():
            self.add_error('library', 'Existing rnc in this library')
        
        return data