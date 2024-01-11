from django.test import TestCase, Client
from django.urls import reverse

from datetime import date

from libraries.models import Rent, Book, Library, BookStatus, BookGenders
from persons.models import Author, Customer, Employee

class IndexViewTests(TestCase):
    def setUp(self):
        self.genders = BookGenders.objects.all()
        self.library1 = Library.objects.create(name = 'libreria1', 
                                               location = 'Tenares',
                                               rnc = '123-1234567-1')
        self.customer1 = Customer.objects.create(first_name='Darwin', 
                                                last_name='Lantigua', 
                                                rnc='402-3070960-8', 
                                                birthday=date(2000, 1, 8), 
                                                library=self.library1)
        self.employee1 = Employee.objects.create(first_name='Darwin', 
                                                last_name='Lantigua', 
                                                rnc='402-3070960-8', 
                                                birthday=date(2000, 1, 8), 
                                                library=self.library1)
        self.author1 = Author.objects.create(first_name = 'Darwin',
                                             last_name = 'Lantigua',
                                             rnc = '402-3070960-8',
                                             birthday = date(2000, 1, 8),
                                             alias = 'Esnaire'
                                             )
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
        self.rent1 = Rent.objects.create(book = self.book1, amount_to_rent = 1,
                                         customer = self.customer1, 
                                         employee = self.employee1, 
                                         library = self.library1,
                                         due_date = date(2025, 6, 12)
                                         )
        self.url = reverse('libraries:rent_index')
        self.client = Client()

    def test_get_index(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Our love is live')
        self.assertContains(response, 'Darwin Lantigua')
        self.assertContains(response, 'libreria1')
        self.assertTemplateUsed(response, 'rent/rent_index.html')

def create_rent(book, amount_to_rent, customer, employee, library, due_date):
    return {
        'book': book,
        'amount_to_rent': amount_to_rent,
        'customer': customer,
        'employee': employee,
        'library': library,
        'due_date': due_date,
    }

class CreateViewTests(TestCase):
    def setUp(self):
        self.genders = BookGenders.objects.all()
        self.library1 = Library.objects.create(name = 'libreria1', 
                                               location = 'Tenares',
                                               rnc = '123-1234567-1')
        self.customer1 = Customer.objects.create(first_name='Darwin', 
                                                last_name='Lantigua', 
                                                rnc='402-3070960-8', 
                                                birthday=date(2000, 1, 8), 
                                                library=self.library1)
        self.employee1 = Employee.objects.create(first_name='Darwin', 
                                                last_name='Lantigua', 
                                                rnc='402-3070960-8', 
                                                birthday=date(2000, 1, 8), 
                                                library=self.library1)
        self.author1 = Author.objects.create(first_name = 'Darwin',
                                             last_name = 'Lantigua',
                                             rnc = '402-3070960-8',
                                             birthday = date(2000, 1, 8),
                                             alias = 'Esnaire'
                                             )
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
        self.url = reverse('libraries:rent_create')
        self.client = Client()

    def test_get_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent/rent_create_form.html')

    def test_valid_data_post(self):
        data = create_rent(self.book1.pk, 1, self.customer1.pk, 
                           self.employee1.pk, self.library1.pk,
                           date(2025, 6, 12))
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent/rent_index.html')

        self.assertEqual(Rent.objects.count(), 1)
        rent_created = Rent.objects.get(book = self.book1)
        self.assertEqual(rent_created.employee, self.employee1)
        self.assertEqual(rent_created.library, self.library1)

    def test_past_due_date(self):
        data = create_rent(self.book1.pk, 1, self.customer1.pk, 
                           self.employee1.pk, self.library1.pk,
                           date(2023, 6, 12))
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(Rent.objects.count(), 0)

    def test_more_books_that_available(self):
        data = create_rent(self.book1.pk, 6, self.customer1.pk, 
                           self.employee1.pk, self.library1.pk,
                           date(2025, 6, 12))
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Rent.objects.count(), 0)
        self.assertTemplateUsed(response, 'rent/rent_create_form.html')

    def test_amount_less_that_1(self):
        data = create_rent(self.book1.pk, 0, self.customer1.pk, 
                           self.employee1.pk, self.library1.pk,
                           date(2025, 6, 12))
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent/rent_create_form.html')
        self.assertEqual(Rent.objects.count(), 0)

    def test_run_out_of_books(self):
        data = create_rent(self.book1.pk, 5, self.customer1.pk, 
                           self.employee1.pk, self.library1.pk,
                           date(2025, 6, 12))
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent/rent_index.html')
        self.assertEqual(Rent.objects.count(), 1)

        self.book1.refresh_from_db()
        self.assertEqual(self.book1.status.name, 'Spent')
        
    def test_dont_run_out_of_books(self):
        data = create_rent(self.book1.pk, 4, self.customer1.pk, 
                           self.employee1.pk, self.library1.pk,
                           date(2025, 6, 12))
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent/rent_index.html')
        self.assertEqual(Rent.objects.count(), 1)

        self.book1.refresh_from_db()
        self.assertEqual(self.book1.status.name, 'Available')

class UpdateViewTests(TestCase):
    def setUp(self):
        self.genders = BookGenders.objects.all()
        self.library1 = Library.objects.create(name = 'libreria1', 
                                               location = 'Tenares',
                                               rnc = '123-1234567-1')
        self.customer1 = Customer.objects.create(first_name='Darwin', 
                                                last_name='Lantigua', 
                                                rnc='402-3070960-8', 
                                                birthday=date(2000, 1, 8), 
                                                library=self.library1)
        self.employee1 = Employee.objects.create(first_name='Darwin', 
                                                last_name='Lantigua', 
                                                rnc='402-3070960-8', 
                                                birthday=date(2000, 1, 8), 
                                                library=self.library1)
        self.author1 = Author.objects.create(first_name = 'Darwin',
                                             last_name = 'Lantigua',
                                             rnc = '402-3070960-8',
                                             birthday = date(2000, 1, 8),
                                             alias = 'Esnaire'
                                             )
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
        self.rent1 = Rent.objects.create(book = self.book1, amount_to_rent = 1,
                                         customer = self.customer1, 
                                         employee = self.employee1, 
                                         library = self.library1,
                                         due_date = date(2025, 6, 12)
                                         )
        self.url = reverse('libraries:rent_update', args=[self.rent1.pk])
        self.client = Client()

    def test_get_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent/rent_update.html')
    
    def test_update_to_past_due_date(self):
        updated_data = create_rent(self.book1.pk, 1, self.customer1.pk, 
                                   self.employee1.pk, self.library1.pk,
                                   date(2023, 6, 12))
        response = self.client.post(self.url, updated_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent/rent_update.html')

    def test_update_to_more_books_that_available(self):
        data = create_rent(self.book1.pk, 6, self.customer1.pk, 
                           self.employee1.pk, self.library1.pk,
                           self.rent1.due_date)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent/rent_update.html')

        self.rent1.refresh_from_db()
        self.assertEqual(self.rent1.amount_to_rent, 1)

    def test_update_to_books_that_available(self):
        data = create_rent(self.book1.pk, 5, self.customer1.pk, 
                           self.employee1.pk, self.library1.pk,
                           self.rent1.due_date)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent/rent_index.html')

        self.rent1.refresh_from_db()
        self.assertEqual(self.rent1.amount_to_rent, 5)

    def test_amount_less_that_1(self):
        data = create_rent(self.book1.pk, 0, self.customer1.pk, 
                           self.employee1.pk, self.library1.pk,
                           self.rent1.due_date)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent/rent_update.html')
        
        self.rent1.refresh_from_db()
        self.assertEqual(self.rent1.amount_to_rent, 1)

    def test_update_and_run_out_of_books(self):
        data = create_rent(self.book1.pk, 5, self.customer1.pk, 
                           self.employee1.pk, self.library1.pk,
                           date(2025, 6, 12))
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent/rent_index.html')
        self.assertEqual(Rent.objects.count(), 1)

        self.book1.refresh_from_db()
        self.assertEqual(self.book1.status.name, 'Spent')
        
    def test_update_and_dont_run_out_of_books(self):
        data = create_rent(self.book1.pk, 4, self.customer1.pk, 
                           self.employee1.pk, self.library1.pk,
                           date(2025, 6, 12))
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent/rent_index.html')
        self.assertEqual(Rent.objects.count(), 1)

        self.book1.refresh_from_db()
        self.assertEqual(self.book1.status.name, 'Available')

class DetailViewTests(TestCase):
    def setUp(self):
        self.genders = BookGenders.objects.all()
        self.library1 = Library.objects.create(name = 'libreria1', 
                                               location = 'Tenares',
                                               rnc = '123-1234567-1')
        self.customer1 = Customer.objects.create(first_name='Darwin', 
                                                last_name='Lantigua', 
                                                rnc='402-3070960-8', 
                                                birthday=date(2000, 1, 8), 
                                                library=self.library1)
        self.employee1 = Employee.objects.create(first_name='Darwin', 
                                                last_name='Lantigua', 
                                                rnc='402-3070960-8', 
                                                birthday=date(2000, 1, 8), 
                                                library=self.library1)
        self.author1 = Author.objects.create(first_name = 'Darwin',
                                             last_name = 'Lantigua',
                                             rnc = '402-3070960-8',
                                             birthday = date(2000, 1, 8),
                                             alias = 'Esnaire'
                                             )
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
        self.rent1 = Rent.objects.create(book = self.book1, amount_to_rent = 1,
                                         customer = self.customer1, 
                                         employee = self.employee1, 
                                         library = self.library1,
                                         rent_date = date(2024, 1, 7),
                                         due_date = date(2024, 6, 12)
                                         )
        self.url = reverse('libraries:rent_detail', args=[self.rent1.pk])
        self.client = Client()

    def test_get_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent/rent_detail.html')
        self.assertEqual(response.context['model'], self.rent1)