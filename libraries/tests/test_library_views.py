from django.test import TestCase, Client
from django.urls import reverse

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

class AddViewTests(TestCase):
    def setUp(self):
        self.url = reverse('libraries:library_add')
        self.client = Client()

    def test_get_add(self):
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

def create_library(name, location, rnc):
    return {
        'name': name,
        'location': location,
        'rnc': rnc,
    }