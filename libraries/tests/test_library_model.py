from django.test import TestCase
from ..models import Library

from mysite.function import validateRnc

class LibraryModelTests(TestCase):
    def test_invalid_rnc(self):
        library = Library(name='libreria1', location='Tenares', rnc='402-30')
        self.assertIs(validateRnc(library.rnc), False)

    def test_valid_rnc(self):
        library1 = Library(name='libreria1', location='Tenares', 
                           rnc='402-3070960-8')
        library2 = Library(name='libreria2', location='Tenares', 
                           rnc='40230709608')
        library3 = Library(name='libreria3', location='Tenares', 
                           rnc='402-30709608')
        library4 = Library(name='libreria4', location='Tenares', 
                           rnc='4023070960-8')
        self.assertIs(validateRnc(library1.rnc), True)
        self.assertIs(validateRnc(library2.rnc), True)
        self.assertIs(validateRnc(library3.rnc), True)
        self.assertIs(validateRnc(library4.rnc), True)