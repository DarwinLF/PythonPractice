from .person_forms import PersonForm
from ..models import Employee

class EmployeeForm(PersonForm):
    class Meta(PersonForm.Meta):
        model = Employee
        fields = PersonForm.Meta.fields + ['library']