from django.test import TestCase, Client
from django.urls import reverse
from django.db import IntegrityError, transaction

from datetime import date

from ..models import Employee
from libraries.models import Library

class IndexViewTests(TestCase):
    def setUp(self):
        self.library = Library.objects.create(name = 'libreria1', 
                                               location = 'Tenares',
                                               rnc = '123-1234567-1')
        self.employee = Employee.objects.create(first_name = 'Darwin',
                                             last_name = 'Lantigua',
                                             rnc = '402-3070960-8',
                                             birthday = date(2000, 1, 8),
                                             library = self.library
                                             )
        self.url = reverse('persons:employee_index')
        self.client = Client()

    def test_get_index(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Darwin')
        self.assertContains(response, 'Lantigua')
        self.assertContains(response, '40230709608')
        self.assertContains(response, 'libreria1')
        self.assertTemplateUsed(response, 'employee/employee_index.html')

def create_employee(first_name, last_name, rnc, birthday, library):
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
        self.url = reverse('persons:employee_create')
        self.client = Client()

    def test_get_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee/employee_create_form.html')

    def test_valid_data_post(self):
        data = create_employee('Darwin', 'Lantigua', '402-3070960-8', 
                               date(2000, 1, 8), self.library.pk)
        response = self.client.post(self.url, data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Employee.objects.count(), 1)
        employee_created = Employee.objects.get(first_name = 'Darwin')
        self.assertEqual(employee_created.last_name, 'Lantigua')
        self.assertEqual(employee_created.rnc, '40230709608')

    def test_duplicate_rnc(self):
        employee = Employee.objects.create(first_name = 'Darwin',
                                           last_name = 'Lantigua',
                                           rnc = '402-3070960-8',
                                           birthday = date(2000, 1, 8),
                                           library = self.library
                                           )

        data = create_employee('Jackson', 'Jonson', '402-30709608', 
                               date(1999, 2, 12), self.library.pk)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee/employee_create_form.html')

        self.assertEqual(Employee.objects.count(), 1)
        self.assertFalse(Employee.objects.filter(first_name='Jackson').exists())

    def test_invalid_rnc(self):
        data = create_employee('Darwin', 'Lantigua', '402-307060-8', 
                               date(2000, 1, 8), self.library.pk)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Employee.objects.count(), 0)
        self.assertFalse(Employee.objects.filter(first_name='Darwin').exists())

    #change in the future
    def test_future_birthday(self):
        data = create_employee('Darwin', 'Lantigua', '402-307060-8', 
                               date(2050, 1, 8), self.library.pk)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(Employee.objects.count(), 0)

    def test_same_employee_same_library(self):
        employee = Employee.objects.create(first_name = 'Darwin',
                                           last_name = 'Lantigua',
                                           rnc = '402-3070960-8',
                                           birthday = date(2000, 1, 8),
                                           library = self.library
                                           )
        data = create_employee('Darwin', 'Lantigua', '402-3070960-8', 
                               date(2000, 1, 8), self.library.pk)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee/employee_create_form.html')
        self.assertEqual(Employee.objects.count(), 1)

    def test_same_employee_different_library(self):
        employee = Employee.objects.create(first_name = 'Darwin',
                                           last_name = 'Lantigua',
                                           rnc = '402-3070960-8',
                                           birthday = date(2000, 1, 8),
                                           library = self.library
                                           )
        library2 = Library.objects.create(name = 'libreria2',
                                          location = 'Salcedo',
                                          rnc = '123-1234567-2')
        data = create_employee('Darwin', 'Lantigua', '402-3070960-8', 
                               date(2000, 1, 8), library2.pk)
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee/employee_index.html')
        self.assertEqual(Employee.objects.count(), 2)

class UpdateViewTests(TestCase):
    def setUp(self):
        self.library = Library.objects.create(name = 'libreria1', 
                                               location = 'Tenares',
                                               rnc = '123-1234567-1')
        self.employee1 = Employee.objects.create(first_name='Darwin', 
                                                 last_name='Lantigua', 
                                                 rnc='402-3070960-8', 
                                                 birthday=date(2000, 1, 8), 
                                                 library=self.library)
        self.employee2 = Employee.objects.create(first_name='Jackson', 
                                                 last_name='Knight', 
                                                 rnc='402-3070960-9', 
                                                 birthday=date(1999, 2, 12), 
                                                 library=self.library)
        self.url = reverse('persons:employee_update', args=[self.employee2.pk])
        self.client = Client()

    def test_get_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee/employee_update.html')

    def test_update_to_duplicate_rnc(self):
        # Submit the form with updated data
        updated_data = create_employee(self.employee2.first_name, 
                                       self.employee2.last_name, 
                                       self.employee1.rnc, 
                                       self.employee2.birthday, 
                                       self.employee2.library.pk)
        response = self.client.post(self.url, updated_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Refresh the person from the database
        self.employee2.refresh_from_db()
        self.assertEqual(self.employee2.rnc, '40230709609')

    def test_update_all_fields_except_rnc(self):
        # Submit the form with updated data
        updated_data = create_employee('Marco', 'Diaz', self.employee2.rnc, 
                                       date(2000, 4, 20), self.library.pk)
        response = self.client.post(self.url, updated_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Refresh the person from the database
        self.employee2.refresh_from_db()
        self.assertEqual(self.employee2.first_name, 'Marco')
        self.assertEqual(self.employee2.last_name, 'Diaz')
        self.assertEqual(self.employee2.rnc, '40230709609')
        self.assertEqual(self.employee2.birthday, date(2000, 4, 20))
        self.assertEqual(self.employee2.library, self.library)

class DetailViewTests(TestCase):
    def setUp(self):
        self.library = Library.objects.create(name = 'libreria1', 
                                               location = 'Tenares',
                                               rnc = '123-1234567-1')
        self.employee = Employee.objects.create(first_name='Darwin', 
                                                last_name='Lantigua', 
                                                rnc='402-3070960-8', 
                                                birthday=date(2000, 1, 8), 
                                                library=self.library)
        self.url = reverse('persons:employee_detail', args=[self.employee.pk])
        self.client = Client()
    
    def test_get_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee/employee_detail.html')
        self.assertEqual(response.context['model'], self.employee)