from django.test import TestCase, Client
from django.urls import reverse

from datetime import date

from libraries.models import Book, Library, BookStatus, BookGenders
from persons.models import Author

class IndexViewTests(TestCase):
    def setUp(self):
        self.genders = BookGenders.objects.all()
        self.author1 = Author.objects.create(first_name = 'Darwin',
                                             last_name = 'Lantigua',
                                             rnc = '402-3070960-8',
                                             birthday = date(2000, 1, 8),
                                             alias = 'Esnaire'
                                             )
        self.library1 = Library.objects.create(name = 'libreria1', 
                                               location = 'Tenares',
                                               rnc = '123-1234567-1')
        self.status = BookStatus.objects.all()
        self.book1 = Book.objects.create(title = 'Our love is live',
                                         published_date = date(2020, 6, 2),
                                         isbn = '123-1-123-12345-1',
                                         gender = self.genders[0],
                                         quantity = 5,
                                         rent_price = 300,
                                         sale_price = 500,
                                         author = self.author1,
                                         library = self.library1,
                                         status = self.status[0],
                                         )
        self.url = reverse('libraries:book_index')
        self.client = Client()

    def test_get_index(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Our love is live')
        self.assertContains(response, 'Darwin Lantigua (Esnaire)')
        self.assertContains(response, 'libreria1')
        self.assertContains(response, 'Available')
        self.assertContains(response, 'Fiction')
        self.assertTemplateUsed(response, 'book/book_index.html')

def create_book(title, published_date, isbn, gender, quantity, rent_price, 
                sale_price, author, library, status):
    return {
        'title': title,
        'published_date': published_date,
        'isbn': isbn,
        'gender': gender,
        'quantity': quantity,
        'rent_price': rent_price,
        'sale_price': sale_price,
        'author': author,
        'library': library,
        'status': status,
    }

class CreateViewTests(TestCase):
    def setUp(self):
        self.genders = BookGenders.objects.all()
        self.author1 = Author.objects.create(first_name = 'Darwin',
                                             last_name = 'Lantigua',
                                             rnc = '402-3070960-8',
                                             birthday = date(2000, 1, 8),
                                             alias = 'Esnaire'
                                             )
        self.library1 = Library.objects.create(name = 'library1', 
                                               location = 'Tenares',
                                               rnc = '123-1234567-1')
        self.status = BookStatus.objects.all()
        self.url = reverse('libraries:book_create')
        self.client = Client()

    def test_get_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/book_create_form.html')

    def test_valid_data_post(self):
        data = create_book('Our love is live', date(2020, 6, 2), 
                           '123-1-123-12345-1', self.genders[0].pk, 5, 300, 
                           500, self.author1.pk, self.library1.pk, 
                           self.status[0].pk)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Book.objects.count(), 1)
        book_created = Book.objects.get(title = 'Our love is live')
        self.assertEqual(book_created.author, self.author1)
        self.assertEqual(book_created.library, self.library1)
        self.assertEqual(book_created.isbn, '1231123123451')

    def test_duplicate_isbn(self):
        book = Book.objects.create(title = 'Our love is live',
                                   published_date = date(2020, 6, 2),
                                   gender = self.genders[0],
                                   isbn = '123-1-123-12345-1',
                                   quantity = 5, rent_price = 300,
                                   sale_price = 500, author = self.author1,
                                   library = self.library1, 
                                   status = self.status[0]
                                   )
        
        data = create_book('Alpha', date(2018, 8, 6), '123-1-12312345-1',
                           self.genders[0].pk, 7, 200, 600, self.author1.pk, 
                           self.library1.pk, self.status[1].pk)
        response = self.client.post(self.url, data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/book_create_form.html')
        self.assertEqual(Book.objects.count(), 1)
        self.assertFalse(Book.objects.filter(title='Alpha').exists())

    def test_invalid_isbn(self):
        data = create_book('Our love is live', date(2020, 6, 2), 
                           '123-1-12-12345-1', self.genders[0].pk, 5, 300, 
                           500, self.author1.pk, self.library1.pk, 
                           self.status[0].pk)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.objects.count(), 0)
        self.assertFalse(Book.objects.filter(title='Our love is live')
                         .exists())

class UpdateViewTests(TestCase):
    def setUp(self):
        self.genders = BookGenders.objects.all()
        self.author1 = Author.objects.create(first_name = 'Darwin',
                                             last_name = 'Lantigua',
                                             rnc = '402-3070960-8',
                                             birthday = date(2000, 1, 8),
                                             alias = 'Esnaire'
                                             )
        self.library1 = Library.objects.create(name = 'library1', 
                                               location = 'Tenares',
                                               rnc = '123-1234567-1')
        self.status = BookStatus.objects.all()
        self.book1 = Book.objects.create(title = 'Our love is live',
                                         published_date = date(2020, 6, 2),
                                         isbn = '123-1-123-12345-1',
                                         gender = self.genders[0],
                                         quantity = 5,
                                         rent_price = 300,
                                         sale_price = 500,
                                         author = self.author1,
                                         library = self.library1,
                                         status = self.status[0]
                                         )
        self.book2 = Book.objects.create(title = 'Alpha',
                                         published_date = date(2020, 6, 2),
                                         isbn = '111-2-333-44444-5',
                                         gender = self.genders[0],
                                         quantity = 7,
                                         rent_price = 200,
                                         sale_price = 600,
                                         author = self.author1,
                                         library = self.library1,
                                         status = self.status[0]
                                         )
        self.url = reverse('libraries:book_update', args=[self.book2.pk])
        self.client = Client()

    def test_get_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/book_update.html')

    def test_update_to_duplicate_isbn(self):
        # Submit the form with updated data
        updated_data = create_book(self.book2.title, 
                                   self.book2.published_date, self.book1.isbn,
                                   self.book2.gender, self.book2.quantity, 
                                   self.book2.rent_price, 
                                   self.book2.sale_price, 
                                   self.book2.author.pk, 
                                   self.book2.library.pk, 
                                   self.book2.status.pk)
        response = self.client.post(self.url, updated_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Refresh the person from the database
        self.book2.refresh_from_db()
        self.assertEqual(self.book2.isbn, '1112333444445')

    def test_update_all_fields_except_isbn(self):
        # Submit the form with updated data
        updated_data = create_book('Blood bond', date(2017, 3, 3), 
                                   self.book2.isbn, self.genders[1].pk, 10, 
                                   150, 300, self.book2.author.pk, 
                                   self.book2.library.pk, self.status[1].pk)
        response = self.client.post(self.url, updated_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/book_index.html')

        # Refresh the person from the database
        self.book2.refresh_from_db()
        self.assertEqual(self.book2.title, 'Blood bond')

class DetailViewTests(TestCase):
    def setUp(self):
        self.genders = BookGenders.objects.all()
        self.author1 = Author.objects.create(first_name = 'Darwin',
                                             last_name = 'Lantigua',
                                             rnc = '402-3070960-8',
                                             birthday = date(2000, 1, 8),
                                             alias = 'Esnaire'
                                             )
        self.library1 = Library.objects.create(name = 'library1', 
                                               location = 'Tenares',
                                               rnc = '123-1234567-1')
        self.status = BookStatus.objects.all()
        self.book = Book.objects.create(title = 'Our love is live',
                                        published_date = date(2020, 6, 2),
                                        isbn = '123-1-123-12345-1',
                                        gender = self.genders[0],
                                        quantity = 5,
                                        rent_price = 300,
                                        sale_price = 500,
                                        author = self.author1,
                                        library = self.library1,
                                        status = self.status[0]
                                        )
        self.url = reverse('libraries:book_detail', args=[self.book.pk])
        self.client = Client()
    
    def test_get_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/book_detail.html')
        self.assertEqual(response.context['model'], self.book)