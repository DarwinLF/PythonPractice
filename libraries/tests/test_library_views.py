from django.test import TestCase, Client
from django.urls import reverse
from django.db import transaction

from ..models import Library

class IndexViewTests(TestCase):
    def setUp(self):
        self.library1 = Library.objects.create(name = 'libreria1', 
                                               location = 'Tenares',
                                               rnc = '123-1234567-1')
        self.url = reverse('libraries:library_index')
        self.client = Client()

    def test_get_index(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'libreria1')
        self.assertContains(response, 'Tenares')
        self.assertContains(response, '12312345671')
        self.assertTemplateUsed(response, 'library/library_index.html')

class CreateViewTests(TestCase):
    def setUp(self):
        self.url = reverse('libraries:library_create')
        self.client = Client()

    def test_get_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'library/library_create_form.html')

    def test_valid_data_post(self):
        data = create_library('libreria2', 'Salcedo', '111-2222222-3')
        response = self.client.post(self.url, data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        try:
            self.assertEqual(Library.objects.count(), 1)
            library_created = Library.objects.get(name = 'libreria2')
            self.assertEqual(library_created.location, 'Salcedo')
            self.assertEqual(library_created.rnc, '11122222223')
        except Library.DoesNotExist:
            self.fail('Library.DoesNotExist: The library you just created does not exist in the database.')

    def test_duplicate_rnc(self):
        # Test POST request 1
        data = create_library('libreria1', 'Tenares', '123-1234567-1')
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Library.objects.filter(name='libreria1').exists())

        # Test POST request 2
        data = create_library('libreria2', 'Salcedo', '123-1234567-1')
        with transaction.atomic():
            response = self.client.post(self.url, data, follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'library/library_create_form.html')

        self.assertFalse(Library.objects.filter(name='libreria2').exists())

    def test_invalid_rnc(self):
        data = create_library('libreria1', 'Tenares', '123-123457-1')
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Library.objects.filter(name='libreria1').exists())

def create_library(name, location, rnc):
    return {
        'name': name,
        'location': location,
        'rnc': rnc,
    }

class UpdateViewTests(TestCase):
    def setUp(self):
        self.library1 = Library.objects.create(name='library1', location='Tenares', rnc='123-1234567-1')
        self.library2 = Library.objects.create(name='library2', location='Salcedo', rnc='111-2222222-3')
        self.url = reverse('libraries:library_update', args=[self.library2.pk])
        self.client = Client()

    def test_get_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'library/library_update.html')

    def test_update_to_duplicate_rnc(self):
        # Submit the form with updated data
        with transaction.atomic():
            updated_data = create_library(self.library2.name, self.library2.location, self.library1.rnc)
            response = self.client.post(self.url, updated_data, follow=True)
            self.assertEqual(response.status_code, 200)

        # Refresh the person from the database
        self.library2.refresh_from_db()
        self.assertEqual(self.library2.rnc, '11122222223')

    def test_update_all_fields_except_rnc(self):
        # Submit the form with updated data
        updated_data = create_library('libreria3', 'Santiago', self.library2.rnc)
        response = self.client.post(self.url, updated_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Refresh the person from the database
        self.library2.refresh_from_db()
        self.assertEqual(self.library2.name, 'libreria3')
        self.assertEqual(self.library2.location, 'Santiago')
        self.assertEqual(self.library2.rnc, '11122222223')