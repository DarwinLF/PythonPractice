from django.test import TestCase, Client
from django.urls import reverse
from django.db import IntegrityError, transaction

from datetime import date

from ..models import Author

class BaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()

class IndexViewTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.author1 = Author.objects.create(first_name = 'Darwin',
                                             last_name = 'Lantigua',
                                             rnc = '402-3070960-8',
                                             birthday = date(2000, 1, 8),
                                             alias = 'Esnaire'
                                             )
        self.url = reverse('persons:author_index')

    def test_get_index(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Darwin')
        self.assertContains(response, 'Lantigua')
        self.assertContains(response, '40230709608')
        self.assertTemplateUsed(response, 'author/author_index.html')

def create_author(first_name, last_name, rnc, birthday, alias):
    return {
        'first_name': first_name,
        'last_name': last_name,
        'rnc': rnc,
        'birthday': birthday,
        'alias': alias,
    }

class CreateViewTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('persons:author_create')

    def test_get_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'author/author_create_form.html')

    def test_valid_data_post(self):
        data = create_author('Darwin', 'Lantigua', '402-3070960-8', 
                             date(2000, 1, 8), 'Esnaire')
        response = self.client.post(self.url, data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Author.objects.count(), 1)
        author_created = Author.objects.get(first_name = 'Darwin')
        self.assertEqual(author_created.last_name, 'Lantigua')
        self.assertEqual(author_created.rnc, '40230709608')

    def test_duplicate_rnc(self):
        self.author1 = Author.objects.create(first_name = 'Darwin',
                                             last_name = 'Lantigua',
                                             rnc = '402-3070960-8',
                                             birthday = date(2000, 1, 8),
                                             alias = 'Esnaire'
                                             )

        data = create_author('Jackson', 'Jonson', '402-3070960-8', 
                             date(1999, 2, 12), 'Jack')
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'author/author_create_form.html')

        self.assertEqual(Author.objects.count(), 1)
        self.assertFalse(Author.objects.filter(first_name='Jackson').exists())

    def test_invalid_rnc(self):
        data = create_author('Darwin', 'Lantigua', '402-307060-8', 
                             date(2000, 1, 8), 'Esnaire')
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Author.objects.count(), 0)
        self.assertFalse(Author.objects.filter(first_name='Darwin').exists())

    #change in the future
    def test_future_birthday(self):
        data = create_author('Darwin', 'Lantigua', '402-307060-8', 
                             date(2050, 1, 8), 'Esnaire')
        response = self.client.post(self.url, data, follow=True)
        self.assertFormError(response, 'form', 'birthday', 
                             'The birthday can\'t be in the future')

class UpdateViewTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.author1 = Author.objects.create(first_name='Darwin', 
                                             last_name='Lantigua', 
                                             rnc='402-3070960-8', 
                                             birthday=date(2000, 1, 8), 
                                             alias='Esnaire')
        self.author2 = Author.objects.create(first_name='Jackson', 
                                             last_name='Knight', 
                                             rnc='402-3070960-9', 
                                             birthday=date(1999, 2, 12), 
                                             alias='Jack')
        self.url = reverse('persons:author_update', args=[self.author2.pk])

    def test_get_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'author/author_update.html')

    def test_update_to_duplicate_rnc(self):
        # Submit the form with updated data
        updated_data = create_author(self.author2.first_name, 
                                     self.author2.last_name, 
                                     self.author1.rnc, 
                                     self.author2.birthday, 
                                     self.author2.alias)
        response = self.client.post(self.url, updated_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Refresh the person from the database
        self.author2.refresh_from_db()
        self.assertEqual(self.author2.rnc, '40230709609')

    def test_update_all_fields_except_rnc(self):
        # Submit the form with updated data
        updated_data = create_author('Marco', 'Diaz', self.author2.rnc, 
                                     date(2000, 4, 20), 'Karate')
        response = self.client.post(self.url, updated_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Refresh the person from the database
        self.author2.refresh_from_db()
        self.assertEqual(self.author2.first_name, 'Marco')
        self.assertEqual(self.author2.last_name, 'Diaz')
        self.assertEqual(self.author2.rnc, '40230709609')
        self.assertEqual(self.author2.birthday, date(2000, 4, 20))
        self.assertEqual(self.author2.alias, 'Karate')

class DetailViewTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.author = Author.objects.create(first_name='Darwin', 
                                            last_name='Lantigua', 
                                            rnc='402-3070960-8', 
                                            birthday=date(2000, 1, 8), 
                                            alias='Esnaire')
        self.url = reverse('persons:author_detail', args=[self.author.pk])
    
    def test_get_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'author/author_detail.html')
        self.assertEqual(response.context['model'], self.author)