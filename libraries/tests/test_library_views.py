from django.test import TestCase, Client
from django.urls import reverse

from libraries.models import Library

class BaseTestCase(TestCase):
    def setUp(self):
        self.library1 = Library.objects.create(name = 'libreria1', 
                                               location = 'Tenares',
                                               rnc = '123-1234567-1')
        self.client = Client()

class IndexViewTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('libraries:library_index')

    def test_get_index(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'libreria1')
        self.assertContains(response, 'Tenares')
        self.assertContains(response, '12312345671')
        self.assertTemplateUsed(response, 'library/library_index.html')

def create_library(name, location, rnc):
    return {
        'name': name,
        'location': location,
        'rnc': rnc,
    }

class CreateViewTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('libraries:library_create')

    def test_get_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'library/library_create_form.html')

    def test_valid_data_post(self):
        data = create_library('libreria2', 'Salcedo', '111-2222222-3')
        response = self.client.post(self.url, data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Library.objects.count(), 2)
        library_created = Library.objects.get(name = 'libreria2')
        self.assertEqual(library_created.location, 'Salcedo')
        self.assertEqual(library_created.rnc, '11122222223')

    def test_duplicate_rnc(self):
        data = create_library('libreria2', 'Salcedo', '123-12345671')
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'library/library_create_form.html')

        self.assertFalse(Library.objects.filter(name='libreria2').exists())
        self.assertEqual(Library.objects.count(), 1)
        self.assertFalse(Library.objects.filter(name='libreria2').exists())

    def test_invalid_rnc(self):
        data = create_library('libreria3', 'Tenares', '123-123457-1')
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Library.objects.filter(name='libreria3').exists())

class UpdateViewTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.library2 = Library.objects.create(name='library2', 
                                               location='Salcedo', 
                                               rnc='111-2222222-3')
        self.url = reverse('libraries:library_update', 
                           args=[self.library2.pk])

    def test_get_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'library/library_update.html')

    def test_update_to_duplicate_rnc(self):
        # Submit the form with updated data
        updated_data = create_library(self.library2.name, 
                                      self.library2.location, 
                                      self.library1.rnc)
        response = self.client.post(self.url, updated_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Refresh the person from the database
        self.library2.refresh_from_db()
        self.assertEqual(self.library2.rnc, '11122222223')

    def test_update_all_fields_except_rnc(self):
        # Submit the form with updated data
        updated_data = create_library('libreria3', 'Santiago', 
                                      self.library2.rnc)
        response = self.client.post(self.url, updated_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Refresh the person from the database
        self.library2.refresh_from_db()
        self.assertEqual(self.library2.name, 'libreria3')
        self.assertEqual(self.library2.location, 'Santiago')
        self.assertEqual(self.library2.rnc, '11122222223')

class DetailViewTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('libraries:library_detail', args=[self.library1.pk])
    
    def test_get_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'library/library_detail.html')
        self.assertEqual(response.context['model'], self.library1)