from .person_forms import PersonForm
from ..models import Author

class AuthorForm(PersonForm):
    class Meta(PersonForm.Meta):
        model = Author
        fields = PersonForm.Meta.fields + ['alias']