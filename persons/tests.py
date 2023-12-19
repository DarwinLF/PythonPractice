from django.test import TestCase, Client
from django.urls import reverse
from django.http import QueryDict
from django.db import IntegrityError

from datetime import date

from .models import Person
from .functions import validateRnc

# Create your tests here.

class PersonModelTests(TestCase):
    def test_invalid_rnc(self):
        person = Person(first_name='Darwin', last_name='Lantigua Fermin', rnc='402-30', birthday=date(2000,1,8))
        self.assertIs(validateRnc(person.rnc), False)

class PersonAddViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_duplicate_rnc(self):
        url = reverse('persons:add')

        #Test GET request
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'persons/person_create_form.html')

        #Test POST request 1
        data = create_person('Darwin', 'Lantigua Fermin', '402-3070960-7', date(2000, 1, 8))
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Person.objects.filter(first_name='Darwin').exists())

        #Test POST request 2
        with self.assertRaises(IntegrityError):
            data = create_person('Jack', 'Michael', '402-30709607', date(1999, 1, 8))
            response = self.client.post(url, data, follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertFalse(Person.objects.filter(first_name='Jack').exists())

    def test_invalid_rnc(self):
        url = reverse('persons:add')

        data1 = create_person('Darwin', 'Lantigua Fermin', '402-307960-', date(2000, 1, 8))
        response1 = self.client.post(url, data1, follow=True)
        self.assertEqual(response1.status_code, 200)
        self.assertFalse(Person.objects.filter(first_name='Darwin').exists())

def create_person(first_name, last_name, rnc, birthday):
    return {
        'first_name': first_name,
        'last_name': last_name,
        'rnc': rnc,
        'birthday': birthday,
    }

class PersonEditViewTest(TestCase):
    def setUp(self):
        self.person1 = Person.objects.create(first_name='Darwin', last_name='Lantigua', rnc='402-3070960-8', birthday=date(2000, 1, 8))
        self.person2 = Person.objects.create(first_name='John', last_name='Doe', rnc='402-3070960-7', birthday=date(1999, 2, 12))
        self.client = Client()

    def test_edit_rnc(self):
        url = reverse('persons:edit', args=[self.person2.pk])

        # Fetch the form for updating the person
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'persons/edit.html')

        # Submit the form with updated data
        with self.assertRaises(IntegrityError):
            updated_data = {
                'first_name': 'John',
                'last_name': 'Doe',
                'rnc': '402-3070960-8',
                'birthday': date(1999, 2, 12)
            }
            response = self.client.post(url, updated_data, follow=True)
            self.assertEqual(response.status_code, 200)

            # Refresh the person from the database
            self.person2.refresh_from_db()
            self.assertEqual(self.person2.rnc, '402-3070960-7')

    def test_edit_all_fields_except_rnc(self):
        url = reverse('persons:edit', args=[self.person2.pk])

        # Fetch the form for updating the person
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'persons/edit.html')

        # Submit the form with updated data
        updated_data = {
            'first_name': 'Jack',
            'last_name': 'Jonson',
            'rnc': '402-3070960-7',
            'birthday': date(1981, 4, 7)
        }
        response = self.client.post(url, updated_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Refresh the person from the database
        self.person2.refresh_from_db()
        self.assertEqual(self.person2.first_name, 'Jack')
        self.assertEqual(self.person2.last_name, 'Jonson')
        self.assertEqual(self.person2.rnc, '40230709607')
        self.assertEqual(self.person2.birthday, date(1981, 4, 7))

class PersonDeleteViewTest(TestCase):
    def setUp(self):
        self.person = Person.objects.create(first_name='Darwin', last_name='Lantigua', rnc='402-3070960-8', birthday=date(2000, 1, 8))
        self.client = Client()

    def test_delete(self):
        url = reverse('persons:deletePerson', args=[self.person.pk])

        # Fetch the form for updating the person
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'persons/confirm_delete.html')

        # Submit the deletion form
        response = self.client.post(url, follow=True)

        # Check if the person is deleted in the database
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'persons/index.html')

        # Ensure the person is no longer in the database
        self.assertFalse(Person.objects.filter(pk=self.person.pk).exists())
        