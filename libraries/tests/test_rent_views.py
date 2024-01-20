from django.test import TestCase, Client
from django.urls import reverse

from datetime import date

from libraries.models import Rent, RentStatus, Book, Library, BookStatus, BookGenders
from persons.models import Author, Customer, CustomerStatus, Employee

class IndexViewTests(TestCase):
    def setUp(self):
        self.library1 = Library.objects.create(name = 'libreria1', 
                                               location = 'Tenares',
                                               rnc = '123-1234567-1')
        self.customerStatus = CustomerStatus.objects.all()
        self.customer1 = Customer.objects.create(first_name = 'Darwin', 
                                                last_name ='Lantigua', 
                                                rnc = '402-3070960-8', 
                                                birthday = date(2000, 1, 8), 
                                                library = self.library1,
                                                credit_time = 7,
                                                status=self.customerStatus[0])
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
        self.bookGenders = BookGenders.objects.all()
        self.bookStatus = BookStatus.objects.all()
        self.book1 = Book.objects.create(title = 'Our love is live',
                                         published_date = date(2020, 6, 2),
                                         isbn = '123-1-123-12345-1',
                                         gender = self.bookGenders[0],
                                         quantity = 5,
                                         rent_price = 300,
                                         sale_price = 500,
                                         author = self.author1,
                                         library = self.library1,
                                         status = self.bookStatus[0]
                                         )
        self.rentStatus = RentStatus.objects.all()
        self.rent1 = Rent.objects.create(book = self.book1, amount_to_rent = 1,
                                         customer = self.customer1, 
                                         employee = self.employee1, 
                                         library = self.library1,
                                         rent_date = date(2024, 1, 18),
                                         due_date = date(2025, 6, 12),
                                         status = self.rentStatus[0]
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

def create_rent(bookPk, amount_to_rent, customerPk, employeePk, libraryPk, 
                rent_date, due_date, statusPk):
    return {
        'book': bookPk,
        'amount_to_rent': amount_to_rent,
        'customer': customerPk,
        'employee': employeePk,
        'library': libraryPk,
        'rent_date': rent_date,
        'due_date': due_date,
        'status': statusPk
    }

class CreateViewTests(TestCase):
    def setUp(self):
        self.library1 = Library.objects.create(name = 'libreria1', 
                                               location = 'Tenares',
                                               rnc = '123-1234567-1')
        self.customerStatus = CustomerStatus.objects.all()
        self.customer1 = Customer.objects.create(first_name='Darwin', 
                                                last_name='Lantigua', 
                                                rnc='402-3070960-8', 
                                                birthday=date(2000, 1, 8), 
                                                library=self.library1,
                                                credit_time = 30,
                                                status=self.customerStatus[0])
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
        self.bookGenders = BookGenders.objects.all()
        self.bookStatus = BookStatus.objects.all()
        self.book1 = Book.objects.create(title = 'Our love is live',
                                         published_date = date(2020, 6, 2),
                                         isbn = '123-1-123-12345-1',
                                         gender = self.bookGenders[0],
                                         quantity = 5,
                                         rent_price = 300,
                                         sale_price = 500,
                                         author = self.author1,
                                         library = self.library1,
                                         status = self.bookStatus[0]
                                         )
        self.rentStatus = RentStatus.objects.all()
        self.url = reverse('libraries:rent_create')
        self.client = Client()

    def test_get_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent/rent_create_form.html')

    def test_valid_data_post(self):
        data = create_rent(self.book1.pk, 1, self.customer1.pk, 
                           self.employee1.pk, self.library1.pk, 
                           date(2024, 1, 18), date(2025, 6, 12), 
                           self.rentStatus[0].pk)
        response = self.client.post(self.url, data, follow=True)
        #import ipdb; ipdb.set_trace()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent/rent_index.html')

        self.assertEqual(Rent.objects.count(), 1)
        rent_created = Rent.objects.get(book = self.book1)
        self.assertEqual(rent_created.employee, self.employee1)
        self.assertEqual(rent_created.library, self.library1)

    def test_past_due_date(self):
        data = create_rent(self.book1.pk, 1, self.customer1.pk, 
                           self.employee1.pk, self.library1.pk,
                           date(2024, 1, 18), date(2023, 6, 12),
                           self.rentStatus[0].pk)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(Rent.objects.count(), 0)

    def test_more_books_that_available(self):
        data = create_rent(self.book1.pk, 6, self.customer1.pk, 
                           self.employee1.pk, self.library1.pk,
                           date(2024, 1, 18), date(2025, 6, 12),
                           self.rentStatus[0].pk)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Rent.objects.count(), 0)
        self.assertTemplateUsed(response, 'rent/rent_create_form.html')

    def test_amount_less_that_1(self):
        data = create_rent(self.book1.pk, 0, self.customer1.pk, 
                           self.employee1.pk, self.library1.pk,
                           date(2024, 1, 18), date(2025, 6, 12),
                           self.rentStatus[0].pk)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent/rent_create_form.html')
        self.assertEqual(Rent.objects.count(), 0)

    def test_run_out_of_books(self):
        data = create_rent(self.book1.pk, 5, self.customer1.pk, 
                           self.employee1.pk, self.library1.pk,
                           date(2024, 1, 18), date(2025, 6, 12),
                           self.rentStatus[0].pk)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent/rent_index.html')
        self.assertEqual(Rent.objects.count(), 1)

        self.book1.refresh_from_db()
        self.assertEqual(self.book1.status.name, 'Spent')
        
    def test_dont_run_out_of_books(self):
        data = create_rent(self.book1.pk, 4, self.customer1.pk, 
                           self.employee1.pk, self.library1.pk,
                           date(2024, 1, 18), date(2025, 6, 12),
                           self.rentStatus[0].pk)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent/rent_index.html')
        self.assertEqual(Rent.objects.count(), 1)

        self.book1.refresh_from_db()
        self.assertEqual(self.book1.status.name, 'Available')

    def test_with_a_overdue_rent(self):
        data1 = create_rent(self.book1.pk, 1, self.customer1.pk, 
                            self.employee1.pk, self.library1.pk,
                            date(2023, 10, 20), date(2024, 6, 12),
                            self.rentStatus[0].pk)
        response = self.client.post(self.url, data1, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent/rent_index.html')
        self.assertEqual(Rent.objects.count(), 1)
        self.customer1.refresh_from_db()
        self.assertEqual(self.customer1.status.name, 'Active Borrower')

        data2 = create_rent(self.book1.pk, 1, self.customer1.pk, 
                            self.employee1.pk, self.library1.pk,
                            date(2024, 1, 20), date(2024, 6, 12),
                            self.rentStatus[0].pk)
        response = self.client.post(self.url, data2, follow=True)

        self.assertEqual(response.status_code, 200)
        #import ipdb; ipdb.set_trace()
        self.assertTemplateUsed(response, 'rent/rent_create_form.html')
        self.assertEqual(Rent.objects.count(), 1)
        self.customer1.refresh_from_db()
        self.assertEqual(self.customer1.status.name, 'Overdue Materials')

    #change the rent_date of data1 in the future
    def test_without_a_overdue_rent(self):
        data1 = create_rent(self.book1.pk, 1, self.customer1.pk, 
                            self.employee1.pk, self.library1.pk,
                            date(2024, 1, 10), date(2024, 6, 12),
                            self.rentStatus[0].pk)
        response = self.client.post(self.url, data1, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent/rent_index.html')
        self.assertEqual(Rent.objects.count(), 1)
        self.customer1.refresh_from_db()
        self.assertEqual(self.customer1.status.name, 'Active Borrower')

        data2 = create_rent(self.book1.pk, 1, self.customer1.pk, 
                            self.employee1.pk, self.library1.pk,
                            date(2024, 1, 15), date(2024, 6, 12),
                            self.rentStatus[0].pk)
        response = self.client.post(self.url, data2, follow=True)

        self.assertEqual(response.status_code, 200)
        #import ipdb; ipdb.set_trace()
        self.assertTemplateUsed(response, 'rent/rent_index.html')
        self.assertEqual(Rent.objects.count(), 2)
        self.customer1.refresh_from_db()
        self.assertEqual(self.customer1.status.name, 'Active Borrower')

class UpdateViewTests(TestCase):
    def setUp(self):
        self.library1 = Library.objects.create(name = 'libreria1', 
                                               location = 'Tenares',
                                               rnc = '123-1234567-1')
        self.customerStatus = CustomerStatus.objects.all()
        self.customer1 = Customer.objects.create(first_name='Darwin', 
                                                last_name='Lantigua', 
                                                rnc = '402-3070960-8', 
                                                birthday = date(2000, 1, 8), 
                                                library = self.library1,
                                                credit_time = 7,
                                                status=self.customerStatus[0])
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
        self.bookGenders = BookGenders.objects.all()
        self.bookStatus = BookStatus.objects.all()
        self.book1 = Book.objects.create(title = 'Our love is live',
                                         published_date = date(2020, 6, 2),
                                         isbn = '123-1-123-12345-1',
                                         gender = self.bookGenders[0],
                                         quantity = 5,
                                         rent_price = 300,
                                         sale_price = 500,
                                         author = self.author1,
                                         library = self.library1,
                                         status = self.bookStatus[0]
                                         )
        self.rentStatus = RentStatus.objects.all()
        self.rent1 = Rent.objects.create(book = self.book1, amount_to_rent = 1,
                                         customer = self.customer1, 
                                         employee = self.employee1, 
                                         library = self.library1,
                                         rent_date = date(2024, 1, 18),
                                         due_date = date(2025, 6, 12),
                                         status = self.rentStatus[0]
                                         )
        self.url = reverse('libraries:rent_update', args=[self.rent1.pk])
        self.client = Client()

    def test_get_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent/rent_update.html')
    
    def test_update_to_past_due_date(self):
        updated_data = create_rent(self.book1.pk, self.rent1.amount_to_rent, 
                                   self.customer1.pk, self.employee1.pk, 
                                   self.library1.pk, self.rent1.rent_date, 
                                   date(2023, 6, 12), self.rent1.status.pk)
        response = self.client.post(self.url, updated_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent/rent_update.html')

    def test_update_to_more_books_that_available(self):
        data = create_rent(self.book1.pk, 6, self.customer1.pk, 
                           self.employee1.pk, self.library1.pk,
                           self.rent1.rent_date, self.rent1.due_date,
                           self.rent1.status.pk)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent/rent_update.html')

        self.rent1.refresh_from_db()
        self.assertEqual(self.rent1.amount_to_rent, 1)

    def test_update_to_books_that_available(self):
        data = create_rent(self.book1.pk, 5, self.customer1.pk, 
                           self.employee1.pk, self.library1.pk,
                           self.rent1.rent_date, self.rent1.due_date,
                           self.rent1.status.pk)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent/rent_index.html')

        self.rent1.refresh_from_db()
        self.assertEqual(self.rent1.amount_to_rent, 5)

    def test_amount_less_that_1(self):
        data = create_rent(self.book1.pk, 0, self.customer1.pk, 
                           self.employee1.pk, self.library1.pk,
                           self.rent1.rent_date, self.rent1.due_date,
                           self.rent1.status.pk)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent/rent_update.html')
        
        self.rent1.refresh_from_db()
        self.assertEqual(self.rent1.amount_to_rent, 1)

    def test_update_and_run_out_of_books(self):
        data = create_rent(self.book1.pk, 5, self.customer1.pk, 
                           self.employee1.pk, self.library1.pk,
                           self.rent1.rent_date, self.rent1.due_date,
                           self.rent1.status.pk)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent/rent_index.html')
        self.assertEqual(Rent.objects.count(), 1)

        self.book1.refresh_from_db()
        self.assertEqual(self.book1.status.name, 'Spent')
        
    def test_update_and_dont_run_out_of_books(self):
        data = create_rent(self.book1.pk, 4, self.customer1.pk, 
                           self.employee1.pk, self.library1.pk,
                           self.rent1.rent_date, self.rent1.due_date,
                           self.rent1.status.pk)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent/rent_index.html')
        self.assertEqual(Rent.objects.count(), 1)

        self.book1.refresh_from_db()
        self.assertEqual(self.book1.status.name, 'Available')

    def test_update_run_out_of_books_to_dont_run_out(self):
        url =  reverse('libraries:rent_create')
        data1 = create_rent(self.book1.pk, 4, self.customer1.pk, 
                           self.employee1.pk, self.library1.pk,
                           date(2024, 1, 18), date(2025, 6, 12),
                           self.rentStatus[0].pk)
        response = self.client.post(url, data1, follow=True)
        
        #import ipdb; ipdb.set_trace()
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.status.name, 'Spent')

        rent2 = Rent.objects.last()

        url =  reverse('libraries:rent_update', args=[rent2.pk])
        data2 = create_rent(self.book1.pk, 3, self.customer1.pk, 
                           self.employee1.pk, self.library1.pk,
                           rent2.rent_date, rent2.due_date,
                           rent2.status.pk)
        response = self.client.post(url, data2, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent/rent_index.html')
        self.assertEqual(Rent.objects.count(), 2)

        self.book1.refresh_from_db()
        self.assertEqual(self.book1.status.name, 'Available')

    def test_return_a_book(self):
        data = create_rent(self.rent1.book.pk, self.rent1.amount_to_rent, self.rent1.customer.pk, 
                           self.rent1.employee.pk, self.rent1.library.pk,
                           self.rent1.rent_date, self.rent1.due_date,
                           self.rentStatus[4].pk)
        response = self.client.post(self.url, data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent/rent_index.html')
        self.assertEqual(Rent.objects.count(), 1)
        self.book1.refresh_from_db()
        #import ipdb; ipdb.set_trace()
        self.assertEqual(self.book1.available(), 5)

class DetailViewTests(TestCase):
    def setUp(self):
        self.library1 = Library.objects.create(name = 'libreria1', 
                                               location = 'Tenares',
                                               rnc = '123-1234567-1')
        self.customerStatus = CustomerStatus.objects.all()
        self.customer1 = Customer.objects.create(first_name='Darwin', 
                                                last_name='Lantigua', 
                                                rnc='402-3070960-8', 
                                                birthday=date(2000, 1, 8), 
                                                library=self.library1,
                                                credit_time = 7,
                                                status=self.customerStatus[0])
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
        self.bookGenders = BookGenders.objects.all()
        self.bookStatus = BookStatus.objects.all()
        self.book1 = Book.objects.create(title = 'Our love is live',
                                         published_date = date(2020, 6, 2),
                                         isbn = '123-1-123-12345-1',
                                         gender = self.bookGenders[0],
                                         quantity = 5,
                                         rent_price = 300,
                                         sale_price = 500,
                                         author = self.author1,
                                         library = self.library1,
                                         status = self.bookStatus[0]
                                         )
        self.rentStatus = RentStatus.objects.all()
        self.rent1 = Rent.objects.create(book = self.book1, amount_to_rent = 1,
                                         customer = self.customer1, 
                                         employee = self.employee1, 
                                         library = self.library1,
                                         rent_date = date(2024, 1, 7),
                                         due_date = date(2024, 6, 12),
                                         status = self.rentStatus[0]
                                         )
        self.url = reverse('libraries:rent_detail', args=[self.rent1.pk])
        self.client = Client()

    def test_get_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent/rent_detail.html')
        self.assertEqual(response.context['model'], self.rent1)