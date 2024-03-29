from django.test import TestCase, Client
from django.urls import reverse
from django.db import IntegrityError, transaction

from datetime import date

from persons.models import Customer, CustomerStatus, Employee, Author
from libraries.models import Library, Rent, RentStatus, Book, BookGenders
from libraries.models import BookStatus

class BaseTestCase(TestCase):
    def setUp(self):
        self.library1 = Library.objects.create(name = 'libreria1', 
                                               location = 'Tenares',
                                               rnc = '123-1234567-1')
        self.library2 = Library.objects.create(name = 'libreria2',
                                               location = 'Salcedo',
                                               rnc = '111-1234567-2')
        self.customerStatus = CustomerStatus.objects.all()
        self.customer1 = Customer.objects.create(first_name = 'Darwin',
                                             last_name = 'Lantigua',
                                             rnc = '402-3070960-8',
                                             birthday = date(2000, 1, 8),
                                             library = self.library1,
                                             credit_time = 7,
                                             status = self.customerStatus[0]
                                             )
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
        self.client = Client()

class IndexViewTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('persons:customer_index')

    def test_get_index(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Darwin')
        self.assertContains(response, 'Lantigua')
        self.assertContains(response, 'libreria1')
        self.assertContains(response, 'Active Borrower')
        self.assertTemplateUsed(response, 'customer/customer_index.html')

    def test_overdue_rent(self):
        rent1 = Rent.objects.create(book = self.book1, 
                                    amount_to_rent = 1,
                                    customer = self.customer1, 
                                    employee = self.employee1, 
                                    library = self.library1,
                                    rent_date = date(2024, 1, 20),
                                    due_date = date(2024, 1, 22),
                                    status = self.rentStatus[0]
                                    )
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/customer_index.html')
        rent1.refresh_from_db()
        self.assertEqual(rent1.status.name, 'Overdue')
        self.assertEqual(response.context['model_list'][0].status.name , 'Overdue Materials')
        self.customer1.refresh_from_db()
        self.assertEqual(self.customer1.status.name, 'Overdue Materials')

def create_customer(first_name, last_name, rnc, birthday, libraryPk, 
                    credit_time, statusPk):
    return {
        'first_name': first_name,
        'last_name': last_name,
        'rnc': rnc,
        'birthday': birthday,
        'library': libraryPk,
        'credit_time': credit_time,
        'status': statusPk
    }

class CreateViewTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('persons:customer_create')

    def test_get_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 
                                'customer/customer_create_form.html')

    def test_valid_data_post(self):
        data = create_customer('Jack', 'Jonson', '402-3070960-7', 
                               date(2000, 1, 8), self.library1.pk, 7,
                               self.customerStatus[0].pk)
        response = self.client.post(self.url, data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Customer.objects.count(), 2)
        customer_created = Customer.objects.last()
        self.assertEqual(customer_created.first_name, 'Jack')
        self.assertEqual(customer_created.last_name, 'Jonson')
        self.assertEqual(customer_created.rnc, '40230709607')

    def test_duplicate_rnc(self):
        data = create_customer('Jackson', 'Jonson', '402-30709608', 
                               date(1999, 2, 12), self.library1.pk, 7,
                               self.customerStatus[0].pk)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 
                                'customer/customer_create_form.html')

        self.assertEqual(Customer.objects.count(), 1)
        self.assertFalse(Customer.objects.filter(first_name=
                                                 'Jackson').exists())

    def test_invalid_rnc(self):
        data = create_customer('Jack', 'Jonson', '402-307060-8', 
                               date(2000, 1, 8), self.library1.pk, 7,
                               self.customerStatus[0].pk)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertFalse(Customer.objects.filter(first_name=
                                                 'Jack').exists())

    #change in the future
    def test_future_birthday(self):
        data = create_customer('Jack', 'Jonson', '402-307060-7', 
                               date(2050, 1, 8), self.library1.pk, 7,
                               self.customerStatus[0].pk)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(Customer.objects.count(), 1)

    def test_same_customer_same_library(self):
        data = create_customer('Darwin', 'Lantigua', '402-3070960-8', 
                               date(2000, 1, 8), self.library1.pk, 7,
                               self.customerStatus[0].pk)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 
                                'customer/customer_create_form.html')
        self.assertEqual(Customer.objects.count(), 1)

    def test_same_customer_different_library(self):
        data = create_customer('Darwin', 'Lantigua', '402-3070960-8', 
                               date(2000, 1, 8), self.library2.pk,
                               7, self.customerStatus[0].pk)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/customer_index.html')
        self.assertEqual(Customer.objects.count(), 2)

class UpdateViewTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.customer2 = Customer.objects.create(first_name='Jackson', 
                                                 last_name='Knight', 
                                                 rnc='402-3070960-9', 
                                                 birthday=date(1999, 2, 12), 
                                                 library=self.library1,
                                                 credit_time = 7,
                                                 status=self.customerStatus[0]
                                                 )
        self.customer3 = Customer.objects.create(first_name='Jackson', 
                                                 last_name='Knight', 
                                                 rnc='402-3070960-9', 
                                                 birthday=date(1999, 2, 12), 
                                                 library=self.library2,
                                                 credit_time = 7,
                                                 status=self.customerStatus[0]
                                                 )
        self.url = reverse('persons:customer_update', 
                           args=[self.customer2.pk])

    def test_get_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/customer_update.html')

    def test_update_to_duplicate_rnc(self):
        # Submit the form with updated data
        updated_data = create_customer(self.customer2.first_name, 
                                       self.customer2.last_name, 
                                       self.customer1.rnc, 
                                       self.customer2.birthday, 
                                       self.customer2.library.pk,
                                       self.customer2.credit_time,
                                       self.customer2.status.pk)
        response = self.client.post(self.url, updated_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Refresh the person from the database
        self.customer2.refresh_from_db()
        self.assertEqual(self.customer2.rnc, '40230709609')

    def test_update_all_fields_except_rnc(self):
        # Submit the form with updated data
        updated_data = create_customer('Marco', 'Diaz', self.customer2.rnc, 
                                       date(2000, 4, 20), self.library1.pk,
                                       8, self.customerStatus[1].pk)
        response = self.client.post(self.url, updated_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Refresh the person from the database
        self.customer2.refresh_from_db()
        self.assertEqual(self.customer2.first_name, 'Marco')
        self.assertEqual(self.customer2.last_name, 'Diaz')
        self.assertEqual(self.customer2.rnc, '40230709609')
        self.assertEqual(self.customer2.birthday, date(2000, 4, 20))
        self.assertEqual(self.customer2.library, self.library1)

    def test_update_same_customer_of_different_library_to_same_library(self):
        updated_data = create_customer(self.customer2.first_name, 
                                       self.customer2.last_name, 
                                       self.customer2.rnc, 
                                       self.customer2.birthday, 
                                       self.library2.pk, 
                                       self.customer2.credit_time,
                                       self.customer2.status.pk)
        response = self.client.post(self.url, updated_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/customer_update.html')

        self.customer2.refresh_from_db()
        self.assertEqual(self.customer2.library, self.library1)

    def test_customer_with_overdue_rent(self):
        rent1 = Rent.objects.create(book = self.book1, 
                                    amount_to_rent = 1,
                                    customer = self.customer2, 
                                    employee = self.employee1, 
                                    library = self.library1,
                                    rent_date = date(2024, 1, 20),
                                    due_date = date(2024, 1, 22),
                                    status = self.rentStatus[0]
                                    )
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/customer_update.html')
        rent1.refresh_from_db()
        self.assertEqual(rent1.status.name, 'Overdue')
        status = CustomerStatus.objects.get(
            pk=response.context['form'].initial['status'])
        self.assertEqual(status.name , 'Overdue Materials')
        self.customer2.refresh_from_db()
        self.assertEqual(self.customer2.status.name, 'Overdue Materials')

class DetailViewTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('persons:customer_detail', 
                           args=[self.customer1.pk])
    
    def test_get_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/customer_detail.html')
        self.assertEqual(response.context['model'], self.customer1)

    def test_overdue_rent(self):
        rent1 = Rent.objects.create(book = self.book1, 
                                    amount_to_rent = 1,
                                    customer = self.customer1, 
                                    employee = self.employee1, 
                                    library = self.library1,
                                    rent_date = date(2024, 1, 20),
                                    due_date = date(2024, 1, 22),
                                    status = self.rentStatus[0]
                                    )
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/customer_detail.html')
        rent1.refresh_from_db()
        self.assertEqual(rent1.status.name, 'Overdue')
        self.assertEqual(response.context['model'].status.name , 'Overdue Materials')
        self.customer1.refresh_from_db()
        self.assertEqual(self.customer1.status.name, 'Overdue Materials')