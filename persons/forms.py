from django import forms
from django.core.exceptions import ValidationError

from .models import Person
from .functions import validateRnc

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
        }

    def as_p(self):
        return self._html_output(
            normal_row='<p%(html_class_attr)s>%(label)s %(field)s%(help_text)s</p>',
            error_row='%s',
            row_ender='</p>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=False,
        )
    
    def clean_rnc(self):
        rnc = self.cleaned_data['rnc']

        if not validateRnc(rnc):
            raise ValidationError('Invalid Rnc')
        
        return rnc
    
    # def clean(self):
    #     data = self.cleaned_data
    #     rnc = data['rnc']

    #     if not validateRnc(rnc):
    #         self.add_error('rnc', 'Invalid Rnc')
        
    #     return data