from django.test import TestCase, Client
from django.urls import reverse
from django.db import IntegrityError, transaction

from datetime import date

from ..models import Customer
from libraries.models import Library

class IndexViewTests(TestCase):
    def setUp(self):
        self.library = Library.objects.create(name = 'libreria1', 
                                               location = 'Tenares',
                                               rnc = '123-1234567-1')
        self.customer = Customer.objects.create(first_name = 'Darwin',
                                             last_name = 'Lantigua',
                                             rnc = '402-3070960-8',
                                             birthday = date(2000, 1, 8),
                                             library = self.library
                                             )
        self.url = reverse('persons:customer_index')
        self.client = Client()

    def test_get_index(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Darwin')
        self.assertContains(response, 'Lantigua')
        self.assertContains(response, '40230709608')
        self.assertContains(response, 'libreria1')
        self.assertTemplateUsed(response, 'customer/customer_index.html')

def create_customer(first_name, last_name, rnc, birthday, library):
    return {
        'first_name': first_name,
        'last_name': last_name,
        'rnc': rnc,
        'birthday': birthday,
        'library': library,
    }

class CreateViewTests(TestCase):
    def setUp(self):
        self.library = Library.objects.create(name = 'libreria1', 
                                               location = 'Tenares',
                                               rnc = '123-1234567-1')
        self.url = reverse('persons:customer_create')
        self.client = Client()

    def test_get_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/customer_create_form.html')

    def test_valid_data_post(self):
        data = create_customer('Darwin', 'Lantigua', '402-3070960-8', 
                               date(2000, 1, 8), self.library.pk)
        response = self.client.post(self.url, data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Customer.objects.count(), 1)
        customer_created = Customer.objects.get(first_name = 'Darwin')
        self.assertEqual(customer_created.last_name, 'Lantigua')
        self.assertEqual(customer_created.rnc, '40230709608')

    def test_duplicate_rnc(self):
        customer = Customer.objects.create(first_name = 'Darwin',
                                           last_name = 'Lantigua',
                                           rnc = '402-3070960-8',
                                           birthday = date(2000, 1, 8),
                                           library = self.library
                                           )

        data = create_customer('Jackson', 'Jonson', '402-30709608', 
                               date(1999, 2, 12), self.library.pk)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/customer_create_form.html')

        self.assertEqual(Customer.objects.count(), 1)
        self.assertFalse(Customer.objects.filter(first_name='Jackson').exists())

    def test_invalid_rnc(self):
        data = create_customer('Darwin', 'Lantigua', '402-307060-8', 
                               date(2000, 1, 8), self.library.pk)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Customer.objects.count(), 0)
        self.assertFalse(Customer.objects.filter(first_name='Darwin').exists())

    #change in the future
    def test_future_birthday(self):
        data = create_customer('Darwin', 'Lantigua', '402-307060-8', 
                               date(2050, 1, 8), self.library.pk)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(Customer.objects.count(), 0)

    def test_same_customer_same_library(self):
        customer = Customer.objects.create(first_name = 'Darwin',
                                           last_name = 'Lantigua',
                                           rnc = '402-3070960-8',
                                           birthday = date(2000, 1, 8),
                                           library = self.library
                                           )
        data = create_customer('Darwin', 'Lantigua', '402-3070960-8', 
                               date(2000, 1, 8), self.library.pk)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/customer_create_form.html')
        self.assertEqual(Customer.objects.count(), 1)

    def test_same_customer_different_library(self):
        customer = Customer.objects.create(first_name = 'Darwin',
                                           last_name = 'Lantigua',
                                           rnc = '402-3070960-8',
                                           birthday = date(2000, 1, 8),
                                           library = self.library
                                           )
        library2 = Library.objects.create(name = 'libreria2',
                                          location = 'Salcedo',
                                          rnc = '123-1234567-2')
        data = create_customer('Darwin', 'Lantigua', '402-3070960-8', 
                               date(2000, 1, 8), library2.pk)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/customer_index.html')
        self.assertEqual(Customer.objects.count(), 2)
    

class UpdateViewTests(TestCase):
    def setUp(self):
        self.library = Library.objects.create(name = 'libreria1', 
                                               location = 'Tenares',
                                               rnc = '123-1234567-1')
        self.customer1 = Customer.objects.create(first_name='Darwin', 
                                                 last_name='Lantigua', 
                                                 rnc='402-3070960-8', 
                                                 birthday=date(2000, 1, 8), 
                                                 library=self.library)
        self.customer2 = Customer.objects.create(first_name='Jackson', 
                                                 last_name='Knight', 
                                                 rnc='402-3070960-9', 
                                                 birthday=date(1999, 2, 12), 
                                                 library=self.library)
        self.url = reverse('persons:customer_update', args=[self.customer2.pk])
        self.client = Client()

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
                                       self.customer2.library.pk)
        response = self.client.post(self.url, updated_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Refresh the person from the database
        self.customer2.refresh_from_db()
        self.assertEqual(self.customer2.rnc, '40230709609')

    def test_update_all_fields_except_rnc(self):
        # Submit the form with updated data
        updated_data = create_customer('Marco', 'Diaz', self.customer2.rnc, 
                                       date(2000, 4, 20), self.library.pk)
        response = self.client.post(self.url, updated_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Refresh the person from the database
        self.customer2.refresh_from_db()
        self.assertEqual(self.customer2.first_name, 'Marco')
        self.assertEqual(self.customer2.last_name, 'Diaz')
        self.assertEqual(self.customer2.rnc, '40230709609')
        self.assertEqual(self.customer2.birthday, date(2000, 4, 20))
        self.assertEqual(self.customer2.library, self.library)

class DetailViewTests(TestCase):
    def setUp(self):
        self.library = Library.objects.create(name = 'libreria1', 
                                               location = 'Tenares',
                                               rnc = '123-1234567-1')
        self.customer = Customer.objects.create(first_name='Darwin', 
                                                last_name='Lantigua', 
                                                rnc='402-3070960-8', 
                                                birthday=date(2000, 1, 8), 
                                                library=self.library)
        self.url = reverse('persons:customer_detail', args=[self.customer.pk])
        self.client = Client()
    
    def test_get_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/customer_detail.html')
        self.assertEqual(response.context['model'], self.customer)