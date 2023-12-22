from django import forms
from django.utils import timezone

from ..models import Library
from mysite.function import validateRnc

class LibraryForm(forms.ModelForm):
    class Meta:
        model = Library
        fields = ['name', 'location', 'rnc']

    # def as_p(self):
    #     return self._html_output(
    #         normal_row='<p%(html_class_attr)s>%(label)s %(field)s%(help_text)s</p>',
    #         error_row='%s',
    #         row_ender='</p>',
    #         help_text_html=' <span class="helptext">%s</span>',
    #         errors_on_separate_row=False,
    #     )
    
    # def clean_rnc(self):
    #     rnc = self.cleaned_data['rnc']

    #     if not validateRnc(rnc):
    #         raise ValidationError('Invalid Rnc')
        
    #     return rnc
    
    def clean(self):
        data = self.cleaned_data
        rnc = data['rnc']

        if not validateRnc(rnc):
            self.add_error('rnc', 'Invalid Rnc')
        
        return data
