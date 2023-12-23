from django.test import TestCase
from ..models import Library

from mysite.function import validateRnc

class LibraryModelTests(TestCase):
    def test_invalid_rnc(self):
        person = Library(name='libreria1', location='Tenares', rnc='402-30')
        self.assertIs(validateRnc(person.rnc), False)