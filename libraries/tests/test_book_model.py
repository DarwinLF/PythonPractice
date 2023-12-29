from django.test import TestCase
from ..models import Book

from datetime import date

from mysite.function import validateIsbn13

class BookModelTests(TestCase):
    def test_invalid_rnc(self):
        book = Book(title='Our love is live', isbn='123-11-12-12345-1')
        self.assertIs(validateIsbn13(book.isbn), False)

    def test_valid_rnc(self):
        book1 = Book(title='Our love is live', isbn='123-1-123-12345-1')
        book2 = Book(title='Our love is live', isbn='1231123123451')
        book3 = Book(title='Our love is live', isbn='1231123-123451')
        book4 = Book(title='Our love is live', isbn='123-1123-123451')
        self.assertIs(validateIsbn13(book1.isbn), True)
        self.assertIs(validateIsbn13(book2.isbn), True)
        self.assertIs(validateIsbn13(book3.isbn), True)
        self.assertIs(validateIsbn13(book4.isbn), True)